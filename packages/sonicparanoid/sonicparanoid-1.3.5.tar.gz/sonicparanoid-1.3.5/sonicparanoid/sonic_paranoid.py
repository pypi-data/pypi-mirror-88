# -*- coding: utf-8 -*-
"""Execute the SonicParanoid."""
import os
import sys
import platform
import pkg_resources
from shutil import copy, rmtree, move, which
import subprocess
import time
from typing import Dict, List, Deque, Any, Tuple, Set
import zipfile
import numpy as np
import gc
import filetype

# IMPORT INTERNAL PACKAGES
from sonicparanoid import ortholog_detection as orthodetect
from sonicparanoid import orthogroups
from sonicparanoid import workers
from sonicparanoid import sys_tools as systools
from sonicparanoid import hdr_mapping as idmapper
from sonicparanoid import remap_tables_c as remap
from sonicparanoid import graph_c as graph
from sonicparanoid import mcl_c as mcl


########### FUNCTIONS ############
def get_params(softVersion):
    """Parse and analyse command line parameters."""
    # create the possible values for sensitivity value
    sensList = []
    for i in range(1, 9):
        sensList.append(float(i))
        for j in range(1, 10):
            fval = float(i + float(j / 10.))
            if fval <= 7.5:
                sensList.append(fval)
    # define the parameter list
    import argparse
    parser = argparse.ArgumentParser(description=f"SonicParanoid {softVersion}",  usage='%(prog)s -i <INPUT_DIRECTORY> -o <OUTPUT_DIRECTORY>[options]', prog="sonicparanoid")

    # Mandatory arguments
    parser.add_argument("-i", "--input-directory", type=str, required=True, help="Directory containing the proteomes (in FASTA format) of the species to be analyzed.", default=None)
    parser.add_argument("-o", "--output-directory", type=str, required=True, help="The directory in which the results will be stored.", default=None)

    # General run options
    parser.add_argument("-p", "--project-id", type=str, required=False, help="Name for the project reflecting the name of run. If not specified it will be automatically generated using the current date and time.", default="")
    parser.add_argument("-sh", "--shared-directory", type=str, required=False, help="The directory in which the alignment files are stored. If not specified it will be created inside the main output directory.", default=None)
    parser.add_argument("-t", "--threads", type=int, required=False, help="Maximum number of CPUs to be used. Default=4", default=4)
    parser.add_argument("-at", "--force-all-threads", required=False, help="Force using all the requested threads.", action="store_true")
    parser.add_argument("-sm", "--skip-multi-species", required=False, help="Skip the creation of multi-species ortholog groups.", default=False, action="store_true")
    parser.add_argument("-d", "--debug", required=False, help="Output debug information. (WARNING: extremely verbose)", default=False, action="store_true")
    parser.add_argument("-nc", "--no-compress", required=False, help="Skip the compression of processed alignment files.", default=False, action="store_true")
    parser.add_argument("-cl", "--compression-lev", type=int, required=False, help="Gzip compression level.\nInteger values between 1 and 9, with 9 and 1 being the highest lowest compression levels, respectively. Default=5", default=5)

    # pairwise orthology inference
    parser.add_argument("-m", "--mode", required=False, help="SonicParanoid execution mode. The default mode is suitable for most studies. Use sensitive or most-sensitive if the input proteomes are not closely related.", choices=["fast", "default", "sensitive", "most-sensitive"], default="default")
    # parser.add_argument("-pm", "--prefilter-mtx", required=False, help="Scoring matrix used by MMseqs2 in the prefilter step. VTML80 might give a slight speed up at the expense of some sensitivity.", choices=["blosum62", "vtml80"], default="blosum62")
    parser.add_argument("-se", "--sensitivity", type=float, required=False, help="Sensitivity for MMseqs2 [1, 7.5]. This will bypass the -m (--mode) parameter.", default=None)
    parser.add_argument("-ml", "--max-len-diff", type=float, required=False, help="Maximum allowed length-difference-ratio between main orthologs and canditate inparalogs.\nExample: 0.5 means one of the two sequences could be two times longer than the other\n 0 means no length difference allowed; 1 means any length difference allowed. Default=0.5", default=0.5)
    parser.add_argument("-db", "--mmseqs-dbs", type=str, required=False, help="The directory in which the database files for MMseqs2 will be stored. If not specified it will be created inside the main output directory.", default=None)
    parser.add_argument("-noidx", "--no-indexing", required=False, help="Avoid the creation of indexes for MMseqs2 databases. IMPORTANT: while this saves starting storage space it makes MMseqs2 slightly slower.\nThe results might also be sligthy different.", default=False, action="store_true")
    parser.add_argument("-op", "--output-pairs", required=False, help="Output a text file with all the orthologous relations.", default=False, action="store_true")
    parser.add_argument("-qfo11", "--qfo-2011", required=False, help="Output a text file with all the orthologous relations formatted to be uploaded to the QfO benchmark service.\nNOTE: implies --output-pairs", default=False, action="store_true")
    parser.add_argument("-ka", "--keep-raw-alignments", required=False, help="Do not delete raw MMseqs2 alignment files. NOTE: this will triple the space required for storing the results.", default=False, action="store_true")
    parser.add_argument("-ca", "--complete-aln", required=False, help="Perform complete alignments.\n", default=False, action="store_true")

    # Ortholog groups inference
    parser.add_argument("-I", "--inflation", type=float, required=False, help="Affects the granularity of ortholog groups. This value should be between 1.2 (very coarse) and 5 (fine grained clustering). Default=1.5", default=1.5)
    parser.add_argument("-slc", "--single-linkage", required=False, help="Use single-linkage-clustering (MultiParanoid-like). NOTE: by default MCL clustering is used.", default=False, action="store_true")
    parser.add_argument("-mgs", "--max-gene-per-sp", type=int, required=False, help="Limits the maximum number of genes per species in the multi-species output table. This option reduces the verbosity of the multi-species output and only affects single-linkage-clustering. Default=150", default=150)

    # Update runs
    parser.add_argument("-ot", "--overwrite-tables", required=False, help="This will force the re-computation of the ortholog tables. Only missing alignment files will be re-computed.", default=False, action="store_true")
    parser.add_argument("-ow", "--overwrite", required=False, help="Overwrite previous runs and execute it again. This can be useful to update a subset of the computed tables.", default=False, action="store_true")
    #parser.add_argument("-u", "--update", type=str, required=False, help="Update the ortholog tables database by adding or removing input proteomes. Performs only required alignments (if any) for new species pairs, and re-compute the ortholog groups.\nNOTE: an ID for the update must be provided.", default=None)
    parser.add_argument("-rs", "--remove-old-species", required=False, help="Remove alignments and pairwise ortholog tables related to species used in a previous run. This option should be used when updating a run in which some input proteomes were modified or removed.", default=False, action="store_true")
    parser.add_argument("-un", "--update-input-names", required=False, help="Remove alignments and pairwise ortholog tables for an input proteome used in a previous which file name conflicts with a newly added species. This option should be used when updating a run in which some input proteomes or their file names were modified.", default=False, action="store_true")

    # parse the arguments
    args = parser.parse_args()

    return (args, parser)


def check_hardware_settings(threads: int, minPerCoreMem: float, debug: bool = False) -> Tuple[int, float]:
    """Check that a given amount of memory is avaliable for each CPU."""
    if debug:
        print("\ncheck_hardware_settings::START")
        print("Threads:\t{:d}".format(threads))
        print("Minimum memory per thread:\t{:.2f}".format(minPerCoreMem))
    from psutil import virtual_memory, cpu_count
    # the hardware information
    availPhysCores: int = cpu_count(logical=False)
    availCores: int = os.cpu_count()
    threadsPerCore: int = int(availCores / availPhysCores)
    availMem: float = round(virtual_memory().total / 1073741824., 2)
    if debug:
        sys.stdout.write("\nSYSTEM INFORMATION:")
        sys.stdout.write("\nTotal physical cores:\t{:d}".format(availPhysCores))
        sys.stdout.write("\nTotal logical CPUs:\t{:d}".format(availCores))
        sys.stdout.write("\nThreads per core:\t{:d}".format(threadsPerCore))
        sys.stdout.write("\nRequested threads:\t{:d}".format(threads))
        sys.stdout.write("\nTotal physical memory:\t{:.2f}".format(availMem))

    # adjust the number of threads is required
    if threads > availCores:
        sys.stderr.write("\nWARNING: the number of logical CPUs requested ({:d}) is higher than the total available logical cores ({:d})".format(threads, availCores))
        sys.stderr.write("\nThe number of threads will be set (at best) to {:d}\n".format(availCores))
        threads = availCores

    # adjust memory per cores
    memPerCore: float = round(availMem / threads, 2)

    # adjust the number of threads if required
    if memPerCore < minPerCoreMem:
        while True:
            threads -= 1
            memPerCore = round(availMem / threads, 2)
            if memPerCore >= minPerCoreMem:
                sys.stdout.write("\n\nINFO")
                sys.stdout.write("\nThe number of threads was set to {:d}".format(threads))
                sys.stdout.write("\nThis allows {:.2f} gigabytes of memory per physical CPU core.".format(memPerCore))
                sys.stdout.write("\nThe suggested minimum memory per CPU core is {:.2f} Gigabytes.\n".format(minPerCoreMem))
                sys.stdout.write("\nNOTE: To use the maximum number of threads regardless of the memory use the flag --force-all-threads\n")
                break
    # return tuple info
    return (threads, memPerCore)



def check_gcc() -> Tuple[str, str, bool]:
    """Check that gcc is installed"""
    gccPath = which("gcc")
    if gccPath != None:
        rOut = subprocess.run("gcc -dumpversion", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        dumpversion:str = rOut.stdout.decode().rstrip()
        # Make sure the version is lower than 9.3 and higher than 3
        # extract the first 2 digits
        tmpstr:str = dumpversion.split(".", 2)[0:2]
        numver:float = float(".".join(tmpstr))
        if not (4 <= numver):
            sys.stderr.write("\nERROR: you must install a version of GCC higher than 4 to use SonicParanoid.\n")
            sys.stderr.write(f"The version installed on your system is {dumpversion}.\n")
            sys.exit(-7)
        # now extract the complete version
        rOut = subprocess.run("gcc -dumpversion", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        version:str = rOut.stdout.decode().rstrip()
        return (version, dumpversion, True)
    else:
        print("ERROR: the gcc compiler was not found on your system!\nYou must install GCC version 4.0 or higher.")
        sys.exit(-7)



def check_mmseqs_installation(root, debug=False):
    """Check if mmseqs has been installed."""
    correctVer: str = "e1a1c1226ef22ac3d0da8e8f71adb8fd2388a249" # as of SonicParanoid 1.3.3
    binDir: str = os.path.join(root, "bin/")
    # zipDir: str = os.path.join(root, "mmseqs2_src/")
    mmseqsPath: str = os.path.join(binDir, "mmseqs")
    # Show info about current version
    if debug:
        print(f"INFO: Current required MMseqs2 version is {correctVer}")
    # copy the zip file if required
    if not os.path.isfile(mmseqsPath):
        copy_mmseqs(root, debug)
    else:
        currentVer: str = ""
        # Check the version
        mmseqsCmd = mmseqsPath
        process = subprocess.Popen(mmseqsCmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout_val, stderr_val = process.communicate() #get stdout and stderr
        process.wait()

        # extract the version
        for ln in stdout_val.decode().split("\n", 7)[:7]:
            if ln[:2] == "MM":
                if ln.startswith("MMseqs2 Ver"):
                    currentVer = ln.rsplit(" ", 1)[-1]
        if debug:
            print(f"MMseqs2 {currentVer} found in\n{mmseqsPath}")
        # Overwrite the file if the version does not match
        if correctVer != currentVer:
            print("\nINFO: a wrong MMseqs2 version is installed, it will be replaced with the appropriate one.")
            # copy the correct binaries
            copy_mmseqs(root, debug)



def copy_mmseqs(root: str, debug: bool=False):
    """Install the proper MMseqs2 binaries"""
    if debug:
        print("copy_mmseqs :: START")
        print(f"Root: {root}")
    binDir: str = os.path.join(root, "bin/")
    zipDir: str = os.path.join(root, "mmseqs2_src/")
    mmseqsPath: str = os.path.join(binDir, "mmseqs")
    # Remove current binaries if already exist
    # final mmseqs path
    if os.path.isfile(mmseqsPath):
        os.remove(mmseqsPath)
        print("Removing previous MMseqs2 binaries...")

    ### Install MMseqs2 ###
    # check operative system
    myOS = platform.system()
    isDarwin: bool = True
    if myOS == "Linux":
        isDarwin = False
    elif myOS == "Darwin":
        isDarwin = True
    sys.stdout.write("\n\n-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-")
    print(f"\nInstalling MMseqs2 binaries for {myOS} system...")
    print("Try the AVX2 version...")
    zipPath: str = ""
    zipName: str = ""
    if isDarwin:
        zipName = "mmseqs_macos_avx2.zip"
        zipPath = os.path.join(zipDir, zipName)
    else:
        zipName = "mmseqs_linux_avx2.zip"
        zipPath = os.path.join(zipDir, zipName)
    # define the unzipped and final paths
    unzippedPath: str = os.path.join(binDir, zipName.rsplit(".", 1)[0])
    # unzip the file
    with zipfile.ZipFile(zipPath, "r") as zip_ref:
        zip_ref.extractall(binDir)

    # rename the unzipped file and change the permissions
    move(unzippedPath, mmseqsPath)
    # change the permission
    os.chmod(mmseqsPath, 0o751)
    # Check if AVX2 is supported
    mmseqsCmd = mmseqsPath
    process = subprocess.Popen(mmseqsCmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout_val, stderr_val = process.communicate() #get stdout and stderr
    del stdout_val
    process.wait()
    # check if an error happened
    mmseqsVersion = "AVX2"
    if len(stderr_val.decode()) > 0:
        print("INFO: Your system does not support the AVX2 instruction set, the SEE4.1 version of MMseqs will be installed...")
        mmseqsVersion = "SSE4.1"
        zipPath = ""
        if isDarwin:
            zipName = "mmseqs_macos_sse41.zip"
            zipPath = os.path.join(zipDir, zipName)
        else:
            zipName = "mmseqs_linux_sse41.zip"
            zipPath = os.path.join(zipDir, zipName)
        # define the unzipped and final paths
        unzippedPath = os.path.join(binDir, zipName.rsplit(".", 1)[0])
        # unzip the file
        with zipfile.ZipFile(zipPath, "r") as zip_ref:
            zip_ref.extractall(binDir)
        # remove binaries if they already exists
        if os.path.isfile(mmseqsPath):
            os.remove(mmseqsPath)
        # rename the unzipped file and change the permissions
        move(unzippedPath, mmseqsPath)
        # change the permission
        os.chmod(mmseqsPath, 0o751)
    # write the final info
    print(f"The MMseqs2 ({mmseqsVersion}) binaries were installed in\n{mmseqsPath}")
    sys.stdout.write("-#-#-#-#-#-#- DONE -#-#-#-#-#-#-\n\n")



def check_mcl_installation(currentDir:str, debug=False) -> bool:
    """Copy or build MCL binaries if required."""
    sonicRoot: str = os.path.dirname(os.path.abspath(__file__))
    if debug:
        print("\ncheck_mcl_installation: START")
        print(f"Running directory: {currentDir}")
        print(f"SonicParanoid root: {sonicRoot}")
    mclroot: str = os.path.join(sonicRoot, "mcl_package/")
    binDir: str = os.path.join(sonicRoot, "bin/")
    systools.makedir(binDir)
    mclTargetPath: str = os.path.join(binDir, "mcl")
    # copy the zip file if required
    if not os.path.isfile(mclTargetPath):
        # First try copying the precompiled binaries
        precompiledOk: bool = copy_precompiled_mcl(mclroot, binDir, debug)
        if precompiledOk:
            return True
        ### Install MCL ###
        # check operative system
        myOS = platform.system()
        sys.stdout.write("\n\n-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-")
        print(f"\nBuilding MCL binaries for {myOS} system...")
        mclTargetPath = compile_mcl(sonicRoot, debug=debug)
        os.chdir(currentDir)
        if not os.path.isfile(mclTargetPath):
            sys.stderr.write("ERROR: the MCL binaries could not be build.\n")
            print("Please contact the developers of SonicParanoid\n{:s}\nor copy working MCL binaries('mcl') in\n{:s}".format("http://iwasakilab.bs.s.u-tokyo.ac.jp/sonicparanoid/", binDir))
            print("More information on MCL can be found at \nhttps://micans.org/mcl/index.html")
            sys.exit(-5)
        else:
            # Copy the compiled binaries into the bin directory
            runout = subprocess.run(f"{mclTargetPath} --version", shell=True)
            if runout.returncode == 0:
                sys.stderr.write(f"\nINFO: MCL installed in\n{mclTargetPath}")
                sys.stdout.write("\n-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-")
                return True
            else:
                print("INFO: something went wrong with the MCL installation.")
                print(f"ERROR code:\t{runout.returncode}")
                print("Please contact the developers of SonicParanoid\n{:s}\nor copy working MCL binaries ('mcl') in\n{:s}".format("http://iwasakilab.bs.s.u-tokyo.ac.jp/sonicparanoid/", binDir))
                print("More information on MCL can be found at \nhttps://micans.org/mcl/index.html")
                sys.exit(-5)
    else: # check if it is working
        process = subprocess.Popen(mclTargetPath, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout_val, stderr_val = process.communicate() #get stdout and stderr
        process.wait()
        # check if an error happened
        stdErrOut: str = stderr_val.decode()
        if stdErrOut[:5] == "[mcl]":
            if debug:
                print(f"MCL binaries found in\n{mclTargetPath}")
            return True
        else:
            # remove the existing binaries
            if os.path.isfile(mclTargetPath):
                os.remove(mclTargetPath)
            # and call the same function to try to copy or build
            os.chdir(currentDir)
            check_mcl_installation(currentDir, debug=debug)



def copy_precompiled_mcl(mclRoot: str, targetDir: str, debug: bool=False) -> bool:
    """Copy precompiled MCL binaries to the target directory."""
    if debug:
        print("\ncopy_precompiled_mcl: START")
        print(f"Directory with MCL binaries: {mclRoot}")
        print(f"Target directory: {targetDir}")

    copyOk: bool = False
    systools.makedir(targetDir)
    # Copy the binaries based on the system
    myOS = platform.system()
    sys.stdout.write("\n-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-")
    print(f"\nCopying MCL binaries for {myOS} system...")
    # Check if the precompike binaries work
    mclTargetPath: str = os.path.join(targetDir, "mcl")
    binaryNames: List[str] = ["mcl_linux"]
    mclFileName: str = ""
    if myOS == "Darwin":
        # mclFileName = "mcl_macos"
        binaryNames: List[str] = ["mcl_darwin_llvm9_clang1103", "mcl_darwin_brew"]
    mclSrcPath: str = ""

    # Test each binary avaliable for the given system
    for mclFileName in binaryNames:
        mclSrcPath = os.path.join(mclRoot, mclFileName)
        # change the permission
        os.chmod(mclSrcPath, 0o751)

        runout = subprocess.run(f"{mclSrcPath} --version", shell=True)
        if runout.returncode != 0:
            sys.stderr.write(f"\nWARNING: the precompile MCL binaries\n{mclSrcPath}\ndo not work on this system.")
            sys.stderr.write(f"\nExit code:\t{runout.returncode}")
            sys.stderr.write(f"\nCMD: {runout.args}\n")
            sys.stdout.write("\n-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-")
            copyOk = False
        else:
            # Remove older binaries if already exist
            if os.path.isfile(mclTargetPath):
                os.remove(mclTargetPath)
            # copy the binaries in the target directory
            copy(mclSrcPath, mclTargetPath)
            # change the permission
            os.chmod(mclTargetPath, 0o751)
            # check again that the copy was successfull
            runout = subprocess.run(f"{mclTargetPath} --version", shell=True)
            if runout.returncode == 0:
                sys.stderr.write(f"\nINFO: MCL binaries copied in\n{mclTargetPath}")
                sys.stdout.write("\n-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-")
                copyOk = True
            else:
                sys.stderr.write(f"\nERROR: something went wrong while copying the MCL binaries in\n{mclTargetPath}\n")
                copyOk = False
    # Return boolean flag
    return copyOk



def count_grps(ogDir:str) -> Tuple[int, int]:
    """Extract number of created groups from stats file"""
    tmpPath:str = os.path.join(ogDir, "overall.stats.tsv")
    ogCnt:int = 0
    scCnt:int = 0
    tmpStr:str = ""
    # extract count of OGs
    if not os.path.isfile(tmpPath):
        sys.stderr.write("\nWARNING: the file with the OG stats was not found!\nMake sure the ortholog groups clustering was successful.")
    else:
        # extract count of OGs
        with open(tmpPath, "r") as ifd:
            for ln in ifd:
                if ln[:6] == "Groups":
                    tmpStr = ln.rsplit("\t", 1)[-1]
                    ogCnt = int(tmpStr.rstrip())
                    break
    # extract count of OGs
    tmpPath = os.path.join(ogDir, "single-copy_groups.tsv")
    if not os.path.isfile(tmpPath):
        sys.stderr.write("\nWARNING: the file with the single-copy OGswas not found!\nMake sure the ortholog groups clustering was successful.")
    else:
        # extract count of single-copy OGs
        with open(tmpPath, "r") as ifd:
            for ln in ifd:
                scCnt += 1
        scCnt -= 1 # this accounts for the header
    return (ogCnt, scCnt)



def compile_mcl(sonicRoot, debug=False):
    """Build MCL binaries"""
    if debug:
        print("compile_mcl :: START")
        print(f"sonicRoot:\t{sonicRoot}")
    # clean the directory from installations
    # Now lets compile MCL
    mclRoot = os.path.join(sonicRoot, "mcl_package")
    buildDir = os.path.join(mclRoot, "mcl_build")
    print("Cleaning up build directory...")
    if os.path.isdir(buildDir):
        rmtree(buildDir)
    systools.makedir(buildDir)
    os.chdir(buildDir)

    # remove old binaries if required
    mclBinDir = os.path.join(buildDir, "bin/")
    if os.path.isdir(mclBinDir):
        print("Cleaning MCL bin directory")
        # remove all its content
        rmtree(mclBinDir)
        systools.makedir(mclBinDir)

    print('\nBuilding MCL clustering algorithm...')
    # check if the archive has been already decompressed
    confPath = os.path.join(buildDir, "configure")
    if os.path.isfile(confPath):
        print('Cleaning any previous installation...')
        # clean configuration
        cleanCmd = 'make distclean'
        process = subprocess.Popen(cleanCmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.communicate() #get stdout and stderr
        process.wait()
        # remove binaries
        cleanCmd = 'make clean'
        process = subprocess.Popen(cleanCmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout_val, stderr_val = process.communicate() #get stdout and stderr
        process.wait()
    else: # extract the archive
        archPath: str = os.path.join(mclRoot, "mcl_src_slim.tar.gz")
        if not os.path.isfile(archPath):
            sys.stderr.write(f"ERROR: the archive with the MCL source code is missing\n{archPath}\nPlease try to download SonicParanoid again.")
            sys.exit(-2)
        else:
            systools.untar(archPath, buildDir, debug=False)
    # configure MCL
    print("\nConfiguring the MCL installation...")
    compileCmd = f"./configure --prefix={buildDir}"
    print(compileCmd)
    process = subprocess.Popen(compileCmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout_val, stderr_val = process.communicate() #get stdout and stderr
    process.wait()

    # binary paths
    mclBin = os.path.join(buildDir, "bin/mcl")
    if os.path.isfile(mclBin):
        print("Removing old MCL binaries...")
        os.remove(mclBin)

    # compile MCL
    compileCmd = 'make install'
    print("Building MCL...")
    print(compileCmd)
    process = subprocess.Popen(compileCmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout_val, stderr_val = process.communicate() #get stdout and stderr
    process.wait()

    print("\nOutput directories info:")
    print("buildDir", buildDir)
    print("mclBinDir", mclBinDir)
    print("mclBin", mclBin)

    if not os.path.isfile(mclBin):
        sys.stderr.write("ERROR: the MCL binaries could not be build.\n")
        sys.exit(-2)

    # reset the current directory
    os.chdir(sonicRoot)
    # Move the binaries to the final target directory
    # Remove older binaries if already exist
    mclTargetPath: str = os.path.join(sonicRoot, "bin/mcl")
    if os.path.isfile(mclTargetPath):
        os.remove(mclTargetPath)
    # copy the binaries in the target directory
    copy(mclBin, mclTargetPath)
    # change the permission
    os.chmod(mclTargetPath, 0o751)
    # remove the build directory
    print("Cleaning up build directory...")
    if os.path.isdir(buildDir):
        rmtree(buildDir)
    sys.stdout.write('-#-#-#-#-#-#- MCL compilation done -#-#-#-#-#-#-\n')
    # reset the current directory
    return mclTargetPath



def extract_single_copy_groups(grpTbl: str, grpFlatTbl: str, debug: bool = False) -> str:
    """Write a list with single copy ortholog groups."""
    if debug:
        print("extract_single_copy_groups :: START")
        print("Input groups table: {:s}".format(grpTbl))
        print("Input \"flast\" groups table: {:s}".format(grpFlatTbl))

    if not os.path.isfile(grpTbl):
      sys.stderr.write("\nERROR: the table with ortholog groups\n{:s}\nwas not found.\n".format(grpTbl))
      sys.exit(-2)
    if not os.path.isfile(grpFlatTbl):
      sys.stderr.write("\nERROR: the table with \"flat\" ortholog groups\n{:s}\nwas not found.\n".format(grpFlatTbl))
      sys.exit(-2)

    # counter for single-copy groups
    scogCnt: int = 0
    rdCnt: int = 0
    # load the first 3 columns only
    ifdFlat = open(grpFlatTbl, "rt")
    ifdGrps = open(grpTbl, "rt")
    # skip the headers
    ifdGrps.readline()
    flatHdr: str = ifdFlat.readline()

    # output paths
    outPath: str = os.path.join(os.path.join(os.path.dirname(grpTbl), "single-copy_groups.tsv"))
    # open output file and write the header
    ofd = open(outPath, "wt")
    ofd.write(flatHdr)

    # now search for single-copy ortholog groups
    # These are groups which a single ortholog for each species in the groups
    for ln in ifdGrps:
        rdCnt += 1
        clstrId, grpSize, spInGrp, d1 = ln.split("\t", 3)
        flatLn: str = ifdFlat.readline()
        del d1
        del clstrId
        if grpSize == spInGrp:
            # then this should be kept
            scogCnt += 1
            ofd.write(flatLn)
    ifdGrps.close()
    ifdFlat.close()
    ofd.close()

    # percentage of single copy ortholog groups
    scogPct: float = round((float(scogCnt)/float(rdCnt)) * 100., 2)
    if debug:
        print("Single-copy ortholog groups:\t{:d}".format(scogCnt))
        print("Percentage of single-copy ortholog groups:\t{:.2f}".format(scogPct))

    # return the output file
    return outPath



def filter_warnings(debug:bool=False):
    """Show warnings only in debug mode"""
    if not debug:
        import warnings
        warnings.filterwarnings("ignore")



def get_mmseqs_supported_version(readmePath):
    """Read a text file and extract the Mmseqs version"""
    if not os.path.isfile(readmePath):
        sys.stderr.write('\nERROR: the file with MMseqs2 version information was not found.\n')
        sys.stderr.write('\nProvided path:\n{:s}\n'.format(readmePath))
        sys.exit(-5)
    # open and read the readme file
    fd = open(readmePath, 'r')
    # skip the first 2 lines...
    fd.readline()
    fd.readline()
    vLine = fd.readline().strip()
    fd.close()
    # return the supported version
    return vLine



def get_input_paths(inDir, debug=False):
    """Check that at least 2 files are provided."""
    # associate a path to each file name
    fname2path = {}
    for f in os.listdir(inDir):
        if f == '.DS_Store':
            continue
        else:
            tmpPath = os.path.join(inDir, f)
            if os.path.isfile(tmpPath):
                fname2path[f] = tmpPath
    # check that at least two input files were provided
    if len(fname2path) < 2:
        sys.stderr.write('ERROR: the directory with the input files only contains {:d} ({:s}) files\nPlease provide at least 2 proteomes.\n'.format(len(fname2path), '\n'.join(list(fname2path.keys()))))
        sys.exit(-5)
    # sort the dictionary by key to avoid different sorting
    # on different systems due to os.listdir()
    sortedDict = dict(sorted(fname2path.items()))
    del fname2path
    return list(sortedDict.values())



def infer_orthogroups_2_proteomes(orthoDbDir: str, outDir: str, sharedDir: str, outName: str, pairsList: List[str], debug: bool=False):
    """Create ortholog groups for only 2 proteomes"""
    import pickle
    if debug:
        print("\ninfer_orthogroups_2_proteomes :: START")

    # sys.exit("DEBUG@sonicparanoid -> infer_orthogroups_2_proteomes")
    # reference species file
    sys.stdout.write('\nCreating ortholog groups for the 2 proteomes...\n')
    timer_start = time.perf_counter()
    # Aux dir
    auxDir: str = os.path.join(sharedDir, "aux")
    # set the output name
    outSonicGroups: str = os.path.join(outDir, outName)
    # extract the only pair
    sp1, sp2 = list(pairsList.keys())[0].split("-", 1)
    tablePath: str = os.path.join(orthoDbDir, f"{sp1}/{sp1}-{sp2}/table.{sp1}-{sp2}")
    flatGrps, notGroupedPath = orthogroups.create_2_proteomes_groups(rawTable=tablePath, outPath=outSonicGroups, debug=debug)
    # load dictionary with protein counts
    seqCntsDict = pickle.load(open(os.path.join(auxDir, 'protein_counts.pckl'), 'rb'))
    # Remap the groups
    sys.stdout.write("\nGenerating final output files...")
    # load dictionary with proteome sizes
    genomeSizesDict = pickle.load(open(os.path.join(auxDir, 'proteome_sizes.pckl'), 'rb'))
    # compute stats
    grpsStatPaths = orthogroups.compute_groups_stats_no_conflict(inTbl=outSonicGroups, outDir=outDir, outNameSuffix="stats", seqCnts=seqCntsDict, proteomeSizes=genomeSizesDict, debug=False)
    # load the mapping information
    id2SpDict, new2oldHdrDict = idmapper.load_mapping_dictionaries(runDir=auxDir, debug=debug)
    # remap the genes in orthogroups
    idmapper.remap_orthogroups(inTbl=outSonicGroups, id2SpDict=id2SpDict, new2oldHdrDict=new2oldHdrDict, removeOld=True, hasConflict=False, debug=debug)
    # remap file with not grouped genes
    idmapper.remap_not_grouped_orthologs(inPath=notGroupedPath, id2SpDict=id2SpDict, new2oldHdrDict=new2oldHdrDict, removeOld=False, debug=debug)
    # remap stats
    idmapper.remap_group_stats(statPaths=grpsStatPaths, id2SpDict=id2SpDict, removeOld=True, debug=debug)
    # remap the flat multi-species table
    idmapper.remap_flat_orthogroups(inTbl=flatGrps, id2SpDict=id2SpDict, new2oldHdrDict=new2oldHdrDict, removeOld=True, debug=debug)
    # extract single-copy ortholog groups
    extract_single_copy_groups(grpTbl=outSonicGroups, grpFlatTbl=flatGrps, debug=debug)
    sys.stdout.write("\nOrtholog groups creation elapsed time (seconds):\t{:s}\n".format(str(round(time.perf_counter() - timer_start, 3))))
    ogCnt, scOgCnt = count_grps(os.path.dirname(flatGrps))
    sys.stdout.write(f"\nOrtholog groups:\t{ogCnt}\n")
    sys.stdout.write(f"Single-copy ortholog groups:\t{scOgCnt}\n")
    print(f"\nThe ortholog groups and related statistics are stored in the directory:\n{os.path.dirname(flatGrps)}")



def infer_orthogroups_qp(orthoDbDir: str, outDir: str, sharedDir: str, sqlTblDir: str, outName: str, pairsList: List[str], maxGenePerSp: int, threads: int=4, debug: bool=False):
    """Perform orthology inference using QuickParanoid."""
    if debug:
        print("\ninfer_orthogroups_qp :: START")
    # reference species file
    sys.stdout.write("\nCreating ortholog groups using single-linkage clustering...")
    multisp_start = time.perf_counter()
    auxDir: str = os.path.join(sharedDir, "aux")
    # seqInfoFilesDir: str = os.path.join(auxDir, "input_seq_info")
    multiParaRunDir: str = os.path.join(outDir, "multiparanoid_run")
    systools.makedir(multiParaRunDir)
    # sys.exit("DEBUG@sonicparanoid -> infer_orthogroups_qp (sql tables creation)")
    # Create SQL tables
    sqlCnt: int = orthogroups.create_sql_tables(orthoDbDir=orthoDbDir, outSqlDir=multiParaRunDir, pairsList=pairsList, threads=threads,  debug=False)
    print(f"{sqlCnt} SQL tables created.")
    quickparaRoot = orthogroups.get_quick_multiparanoid_src_dir()
    #create the multi-species clusters
    orthoGrps, grpsStatPaths = orthogroups.run_quickparanoid(tblList=pairsList, sqlTblDir=multiParaRunDir, outDir=multiParaRunDir, sharedDir=auxDir, srcDir=quickparaRoot, outName=outName, maxGenePerSp=40, debug=False)
    # Move files to the main output directory
    for k, fpath in grpsStatPaths.items():
        move(fpath, outDir)
        grpsStatPaths[k] = os.path.join(outDir, os.path.basename(fpath))
    move(orthoGrps, outDir)
    ogsFileName = os.path.basename(orthoGrps)
    move(os.path.join(os.path.dirname(orthoGrps), f"flat.{ogsFileName}"), outDir)
    move(os.path.join(os.path.dirname(orthoGrps), f"not_assigned_genes.{ogsFileName}"), outDir)
    orthoGrps = os.path.join(outDir, ogsFileName)
    rmtree(multiParaRunDir, ignore_errors=True)
    # load the mapping information
    id2SpDict, new2oldHdrDict = idmapper.load_mapping_dictionaries(runDir=auxDir, debug=debug)
    # remap the genes in orthogroups
    idmapper.remap_orthogroups(inTbl=orthoGrps, id2SpDict=id2SpDict, new2oldHdrDict=new2oldHdrDict, removeOld=True, hasConflict=True, debug=debug)
    # remap the flat multi-species table
    flatGrps = os.path.join(outDir, f"flat.{ogsFileName}")
    idmapper.remap_flat_orthogroups(inTbl=flatGrps, id2SpDict=id2SpDict, new2oldHdrDict=new2oldHdrDict, removeOld=True, debug=debug)
    # remap file with not grouped genes
    notGroupedPath = os.path.join(outDir, f"not_assigned_genes.{ogsFileName}")
    idmapper.remap_not_grouped_orthologs(inPath=notGroupedPath, id2SpDict=id2SpDict, new2oldHdrDict=new2oldHdrDict, removeOld=True, debug=debug)
    # remap stats
    idmapper.remap_group_stats(statPaths=grpsStatPaths, id2SpDict=id2SpDict, removeOld=True, debug=debug)
    # extract single-copy ortholog groups
    extract_single_copy_groups(grpTbl=orthoGrps, grpFlatTbl=flatGrps, debug=debug)
    sys.stdout.write(f"Ortholog groups creation elapsed time (seconds):\t{round(time.perf_counter() - multisp_start, 3)}\n")
    ogCnt, scOgCnt = count_grps(os.path.dirname(outDir))
    sys.stdout.write(f"\nOrtholog groups:\t{ogCnt}\n")
    sys.stdout.write(f"Single-copy ortholog groups:\t{scOgCnt}\n")
    print(f"\nThe ortholog groups and related statistics are stored in the directory:\n{outDir}")



def infer_orthogroups_mcl(orthoDbDir: str, outDir: str, sharedDir: str, sqlTblDir: str, outName: str, pairsList: List[str], inflation: float = 1.5, maxGenePerSp: int = 150, threads: int=4, debug: bool=False):
    """Perform orthology inference using MCL"""
    import pickle
    if debug:
        print("\ninfer_orthogroups_mcl :: START")
    
    # sys.exit("DEBUG@sonicparanoid -> infer_orthogroups_mcl")
    auxDir: str = os.path.join(sharedDir, "aux")
    sys.stdout.write("\nCreating ortholog groups using MCL clustering...")
    timer_start = time.perf_counter()
    # compute ortholog matrixes
    mtxDir = os.path.join(orthoDbDir, "matrixes")
    systools.makedir(mtxDir)
    # create matrixes
    graph.create_matrix_from_orthotbl_parallel(pairsList=pairsList, runDir=auxDir, orthoDbDir=orthoDbDir, outDir=mtxDir, threads=threads, debug=False)
    # call garbage collector
    gc.collect()
    # load dictionary with protein counts
    seqCntsDict = pickle.load(open(os.path.join(auxDir, "protein_counts.pckl"), "rb"))
    # path for the matrix with combination
    combMtxPath = os.path.join(auxDir, "combination_mtx.npz")
    # merge the inparalog matrixes
    spArray = np.array([int(x) for x in seqCntsDict.keys()], dtype=np.uint16)
    # start timer
    tmp_timer_start = time.perf_counter()
    sys.stdout.write("\nMerging inparalog matrixes...")
    graph.merge_inparalog_matrixes_parallel(spArray, combMtxPath, inDir=mtxDir, outDir=mtxDir, threads=threads, removeMerged=True, debug=False)
    sys.stdout.write("\nInparalogs merging elapsed time (seconds):\t{:s}\n".format(str(round(time.perf_counter() - tmp_timer_start, 3))))
    # create MCL output dir
    mclDir = os.path.join(sharedDir, "ortholog_groups")
    systools.makedir(mclDir)
    # Create MCL files
    # THIS NEEDS TO BE IMPLEMENTED FOR SUBGROUPS OF SPECIES
    emptyArray = np.array(np.arange(start=1, stop=1, step=1, dtype=np.int16))
    # create MCL matrix
    sys.stdout.write("\nCreating input matrix for MCL...")
    tmp_timer_start = time.perf_counter()
    mclMatrix = mcl.write_mcl_matrix(spArray, spSkipArray=emptyArray, runDir=auxDir, mtxDir=mtxDir, outDir=mclDir, threads=threads, removeProcessed=True, debug=False)
    sys.stdout.write(f"\nMCL graph creation elapsed time (seconds):\t{round(time.perf_counter() - tmp_timer_start, 3)}\n")
    # output paths
    rawMclGroupsPath = os.path.join(mclDir, f"raw_mcl_{outName}")
    # Run MCL
    sys.stdout.write("\nRunning MCL...")
    sys.stdout.flush()
    tmp_timer_start = time.perf_counter()
    mcl.run_mcl(mclGraph=mclMatrix, outPath=rawMclGroupsPath, inflation=inflation, threads=threads, removeInput=False, debug=debug)
    sys.stdout.write(f"\nMCL execution elapsed time (seconds):\t{round(time.perf_counter() - tmp_timer_start, 3)}\n")
    # remap the orthogroups
    outSonicGroups = os.path.join(mclDir, outName)
    # Remap the groups
    sys.stdout.write("\nGenerating final output files...")
    tmp_timer_start = time.perf_counter()
    mcl.remap_mcl_groups(mclGrps=rawMclGroupsPath, outPath=outSonicGroups, runDir=auxDir, writeFlat=True, debug=debug)
    # load dictionary with proteome sizes
    genomeSizesDict = pickle.load(open(os.path.join(auxDir, "proteome_sizes.pckl"), "rb"))
    # compute stats
    grpsStatPaths = orthogroups.compute_groups_stats_no_conflict(inTbl=outSonicGroups, outDir=mclDir, outNameSuffix="stats", seqCnts=seqCntsDict, proteomeSizes=genomeSizesDict, debug=debug)
    # load the mapping information
    id2SpDict, new2oldHdrDict = idmapper.load_mapping_dictionaries(runDir=auxDir, debug=debug)
    # remap the genes in orthogroups
    idmapper.remap_orthogroups(inTbl=outSonicGroups, id2SpDict=id2SpDict, new2oldHdrDict=new2oldHdrDict, removeOld=True, hasConflict=False, debug=debug)
    # remap file with not grouped genes
    notGroupedPath = os.path.join(mclDir, f"not_assigned_genes.{outName}")
    idmapper.remap_not_grouped_orthologs(inPath=notGroupedPath, id2SpDict=id2SpDict, new2oldHdrDict=new2oldHdrDict, removeOld=True, debug=debug)
    # remap stats
    idmapper.remap_group_stats(statPaths=grpsStatPaths, id2SpDict=id2SpDict, removeOld=True, debug=debug)
    # remap the flat multi-species table
    flatGrps = os.path.join(mclDir, f"flat.{outName}")
    idmapper.remap_flat_orthogroups(inTbl=flatGrps, id2SpDict=id2SpDict, new2oldHdrDict=new2oldHdrDict, removeOld=True, debug=debug)
    # extract single-copy ortholog groups
    extract_single_copy_groups(grpTbl=outSonicGroups, grpFlatTbl=flatGrps, debug=debug)
    sys.stdout.write("\nElapsed time for the creation of final output (seconds):\t{:s}\n".format(str(round(time.perf_counter() - tmp_timer_start, 3))))
    del tmp_timer_start
    sys.stdout.write("Ortholog groups creation elapsed time (seconds):\t{:s}\n".format(str(round(time.perf_counter() - timer_start, 3))))
    ogCnt, scOgCnt = count_grps(mclDir)
    sys.stdout.write(f"\nOrtholog groups:\t{ogCnt}\n")
    sys.stdout.write(f"Single-copy ortholog groups:\t{scOgCnt}\n")
    print(f"\nThe ortholog groups and related statistics are stored in the directory:\n{mclDir}")



def write_run_info_file(infoDir, infoDict, debug=False) -> str:
    """Write a file summarizing the run settings."""
    if debug:
        print("\nwrite_run_info_file :: START")
        print(f"Directory with run info: {infoDir}")
    infoFile: str = os.path.join(infoDir, "run_info.txt")
    ofd = open(infoFile, "w")
    for info, val in infoDict.items():
        if info == "Version":
            ofd.write(f"SonicParanoid {val}\n")
        else:
            ofd.write(f"{info}\t{val}\n")
    ofd.close()
    return infoFile



def sanity_check(infoDict: Dict[str, str], debug:bool=False) -> bool:
    """
    Make sure there are no uncompleted alignments from previous runs.
    Avoid runs using different sensitivity settings.
    Compress/extract alignment files before starting the run.
    """
    updateRun:str = infoDict["Update run:"]
    completeOw:str = infoDict["Complete overwrite:"]
    if debug:
        print("\nsanity_check :: START")
        print(f"Update run:\t{updateRun}")
        print(f"Complete overwrite:\t{completeOw}")

    if updateRun == "False":
        return True
    else:
        # Just return True as no everything will be overwritten anyway
        if completeOw == "True":
            return True

    # Extract information from previous run
    # and check for inconstencies in parameters
    outRoot:str = infoDict["Output directory:"]
    prevRunFile:str = os.path.join(outRoot, "last_run_info.txt")
    threads: int = int(infoDict["Threads:"])
    compress: bool = False if (infoDict["Compress alignments:"] == "False") else True
    complev:int = 5 if (not compress) else int(infoDict["Compression level:"])

    if not os.path.isfile(prevRunFile):
        sys.stderr.write(f"\nWARNING: the file with info on previous run\n{prevRunFile}\nwas not found.\nThis might cause some inconsistency with previous results if some files were unadvertedly deleted by the user.\n")
    else:
        currentSens: str = infoDict["MMseqs sensitivity:"]
        currentMl: str = infoDict["Max length difference for in-paralogs:"]
        currentInfl: str = infoDict["MCL inflation:"]
        prevVal: str = ""

        # parse and extract info from the run info file
        with open(prevRunFile, "rt") as ifd:
            for ln in ifd:
                # extract from 'MMseqs sensitivity'
                if ln[0:8] == "MMseqs s":
                    prevVal = ln.rsplit("\t", 1)[-1].rstrip("\n")
                    if prevVal != currentSens:
                        sys.stderr.write(f"\nERROR: the MMseqs sensitivity ({currentSens}) is different from the one used in the previous run ({prevVal}).\n")
                        sys.stderr.write(f"This is not allowed as it would generate unconsistent results.\nSet the same MMseqs sensitivity ({prevVal}) or use the '-ow' parameter to start a new run with the desired sensitivity ({currentSens}).\n")
                        sys.stderr.write(f"Be aware that this would overwrite all the previously generatet all-vs-all alignments.\n")
                        sys.stderr.flush()
                        sys.exit(-4)
                # extract from 'Max length difference for in-paralogs'
                elif ln[0:2] == "Ma":
                    prevVal = ln.rsplit("\t", 1)[-1].rstrip("\n")
                    if prevVal != currentMl:
                        sys.stdout.write(f"\nINFO: the current '-ml' parameter ({currentMl}) is different from the one used in the previous run ({prevVal}).\nThis might generate slighty different results.\n")
                # extract from 'MCL inflation'
                elif ln[0:2] == "MC":
                    prevVal = ln.rsplit("\t", 1)[-1].rstrip("\n")
                    if prevVal != currentInfl:
                        sys.stdout.write(f"\nINFO: the current MCL inflation parameter '-I' ({currentInfl}) is different from the one used in the previous run ({prevVal}).\nThis might generate slighty different ortholog groups.\n")

    # Obtain some required information
    ortoDbDir:str = infoDict["Pairwise tables DB directory:"]
    alnDir:str = infoDict["Alignment directory:"]
    tmpAlnSpDir:str = ""
    # Paths used for compression/extraction
    tmpAlnPath:str = ""
    tmpSanityPath:str = ""
    sanityDir:str = os.path.join(alnDir, "tmp_sanity_check")
    tmpSanityDir:str = ""
    # remove the directory if already exists, and create it again
    if os.path.isdir(sanityDir):
        rmtree(sanityDir)
    systools.makedir(sanityDir)
    # will contains the path for which compression or decompression is required
    archivingJobs: List[Tuple[str, str]] = []
    spFile:str = os.path.join(infoDict["Run directory:"], "aux/species.tsv")
    spList:List[int] = []
    rmPairSet:Set[str] = set()
    # counter for removed alignments
    rmDirCnt = rmFileCnt = 0
    from itertools import combinations_with_replacement
    # itertools.combinations(spList, r=2)
    # read the species IDs and generate the cobinations
    with open(spFile, "rt") as ifd:
        spList = [ln.split("\t", 1)[0] for ln in ifd]

    # Simplified version using os.walk()
    for sp in spList:
        tmpAlnSpDir = os.path.join(alnDir, sp)
        for r, dirs, files in os.walk(tmpAlnSpDir, topdown=True):
            # remove directories
            for tmpDir in dirs:
                rmtree(os.path.join(r, tmpDir))
                rmPairSet.add(tmpDir)
                rmDirCnt += 1
            # remove alignments files or compress decompress alignment files
            for tmpName in files:
                tmpAlnPath = os.path.join(r, tmpName)
                # remove alignments files before the renaiming e.g., '_1-2'
                if tmpName[0] == "_":
                    os.remove(tmpAlnPath)
                    rmPairSet.add(tmpName[1:])
                    rmFileCnt += 1
                # add compress/extract jobs depending on the matched condition
                elif (compress and (not filetype.is_archive(tmpAlnPath))) or ((not compress) and filetype.is_archive(tmpAlnPath)):
                    # print(tmpAlnPath)
                    tmpSanityDir = os.path.join(sanityDir, sp)
                    systools.makedir(tmpSanityDir)
                    tmpSanityPath = os.path.join(tmpSanityDir, tmpName)
                    # move the file, and add the compress job
                    move(tmpAlnPath, tmpSanityDir)
                    archivingJobs.append((tmpSanityPath, tmpAlnPath))
            break

    # perform the compression\extraction jobs
    if len(archivingJobs) > 0:
        # [print(el) for el in archivingJobs]
        workers.parallel_archive_processing(archivingJobs, complev=complev, removeSrc=True, threads=threads, compress=compress, debug=debug)

    # Remove directory with tmp sanity check files
    if os.path.isdir(os.path.join(ortoDbDir, "matrixes")):
        rmtree(os.path.join(ortoDbDir, "matrixes"))

    # Remove directory with ortholog matrixes
    if os.path.isdir(sanityDir):
        rmtree(sanityDir)

    # show some debug
    if debug:
        print(f"Checked alignments for {len(spList)} species")
        print(f"Removed alignment directories:\t{rmDirCnt}")
        print(f"Removed alignment files before renaming:\t{rmFileCnt}")
        print(f"Pairs with imcomplete alignment runs:\t{len(rmPairSet)}")
        print(f"Compressed/extracted files:\t{len(archivingJobs)}")



def set_project_id(rId: str="", runsDir: str=os.getcwd(), args: Any=None, debug=False):
    """Generates a run ID if required."""
    if debug:
        print("\nset_project_id :: START")
        print("Run name:\t{:s}".format(rId))
        print("Runs directory: {:s}".format(runsDir))
    if not os.path.isdir(runsDir):
        sys.stderr.write('\nERROR: the directory with the runs does not exist.\n')
        sys.exit(-2)
    # create the runid if required
    if len(rId) == 0:
        ltime = time.localtime(time.time())
        # the id should include:
        # day of the month: tm_mday
        # month of the year: tm_mon
        # 2-digits year: tm_year
        # hours: tm_hour
        # minutes: tm_min
        # seconds: tm_sec
        startTime = "{:d}{:d}{:s}{:d}{:d}{:d}".format(ltime.tm_mday, ltime.tm_mon, str(ltime.tm_year)[2:], ltime.tm_hour, ltime.tm_min, ltime.tm_sec)
        rId = "sonic_{:s}".format(startTime)
        # add additional information to the run id name
        runMode = args.mode
        if not args.sensitivity is None:
            runMode = "custom{:s}".format("".join(str(args.sensitivity).split(".", 1)))
        rId = "{:s}_{:s}_{:d}cpus_ml{:s}".format(rId, runMode, args.threads, "".join(str(args.max_len_diff).split(".", 1)) )
        # add other extra info in the naming
        if args.no_indexing:
            rId = "{:s}_noidx".format(rId)
        if args.overwrite:
            rId = "{:s}_ow".format(rId)
        if args.overwrite_tables:
            if not args.overwrite:
                rId = "{:s}_ot".format(rId)
        if args.output_pairs:
            rId = "{:s}_op".format(rId)
        if args.skip_multi_species:
            rId = "{:s}_sm".format(rId)
        if args.debug:
            rId = "{:s}_d".format(rId)

    else: # check that the ID was not previously used
        for f in os.listdir(runsDir):
            if f.startswith('.DS_'):
                continue
            tmpPath = os.path.join(runsDir, f)
            if os.path.isdir(tmpPath):
                if f == rId:
                    sys.stderr.write('\nERROR: the run ID {:s} was used in a previous run.\n'.format(f))
                    sys.stderr.write('Remove the previous run or choose a different run ID.\n')
                    sys.exit(-5)
    return rId



########### MAIN ############
def main():
    # set the minimum memory required per thread
    minPerCoreMem: float = 1.75
    # Extract info about GCC compiler
    gccInfoTpl = check_gcc() 
    # check that everything was installed correctly
    root = os.path.dirname(os.path.abspath(__file__))
    # get SonicParanoid version
    softVersion = pkg_resources.get_distribution("sonicparanoid").version
    # settings for the hashing algorithm
    hashAlgo = "sha256"
    hashBits = 256
    # Will contain information to be printed in the info file
    infoDict: Dict[str, str] = {}
    # start measuring the execution time
    ex_start = time.perf_counter()
    #Get the parameters
    args, parser = get_params(softVersion)
    # start setting the needed variables
    debug = args.debug
    # compression settings
    noCompress: bool = args.no_compress
    complev: int = args.compression_lev # Filter warnings
    # Check compression level
    if (complev < 1) or (complev > 9):
        sys.stderr.write(f"\nWARNING: The complev parameter must be between 1 and 9 while it was set to {complev}\n")
        sys.stderr.write("It will be set to the default [complev=5].\n")
        complev = 5
    # Set warning level
    filter_warnings(debug)
    # perform normal alignments
    complete_aln: bool = args.complete_aln
    # check MMseqs2 installation
    check_mmseqs_installation(root, debug=debug)
    # check MCL installation
    check_mcl_installation(os.getcwd(), debug=debug)
    # set main directories
    inDir = None
    if args.input_directory is not None:
        inDir = f"{os.path.realpath(args.input_directory)}/"
    # output dir
    outDir = os.path.realpath(args.output_directory)
    # check that the input directory has been provided
    if (inDir is None):
        sys.stderr.write("\nERROR: no input species.\n")
        parser.print_help()
    # obtain input paths
    inPaths = get_input_paths(inDir, debug=debug)

    # Pair-wise tables directory
    pairwiseDbDir = os.path.join(outDir, "orthologs_db/")
    systools.makedir(pairwiseDbDir)
    # Runs directory
    runsDir = os.path.join(outDir, "runs/")
    systools.makedir(runsDir)
    # set the update variable
    update_run = False
    # check that the snapshot file exists
    snapshotFile = os.path.join(outDir, "snapshot.tsv")
    if update_run:
        # check that it is not the first run
        if not os.path.isfile(snapshotFile):
            sys.stderr.write("\nWARNING: no snapshot file found. The run will considered as the first one.\n")
            update_run = False
    else:
        # force the variable to true if a snapshot exists
        if os.path.isfile(snapshotFile):
            update_run = True

    # Optional directories setup
    alignDir = None
    if args.shared_directory is not None:
        alignDir = os.path.realpath(args.shared_directory)
    else:
        alignDir = os.path.join(outDir, "alignments/")
        systools.makedir(alignDir)
    dbDirectory = None
    if args.mmseqs_dbs is not None:
        dbDirectory = os.path.realpath(args.mmseqs_dbs)
    else:
        dbDirectory = os.path.join(outDir, "mmseqs2_databases/")
    threads = args.threads
    #coff = args.cutoff
    coff = 40
    owOrthoTbls = args.overwrite_tables
    skipMulti = args.skip_multi_species
    runMode = args.mode
    slc: bool = args.single_linkage
    maxGenePerSp = args.max_gene_per_sp
    # set the sensitivity value for MMseqs2
    sensitivity = 4.0 # default
    if runMode == 'sensitive':
        sensitivity = 6.0
    elif runMode == 'fast':
        sensitivity = 2.5
    elif runMode == 'most-sensitive':
        sensitivity = 7.5
    overwrite = args.overwrite
    if overwrite:
        owOrthoTbls = True
        # remove all the mmseqs2 index files
        if os.path.isdir(dbDirectory):
            for f in os.listdir(dbDirectory):
                fpath = os.path.join(dbDirectory, f)
                try:
                    if os.path.isfile(fpath):
                        os.unlink(fpath)
                    elif os.path.isdir(fpath): rmtree(fpath)
                except Exception as e:
                    print(e)

    # set sensitivity using a user spcified value if needed
    if args.sensitivity:
        if 1. <= args.sensitivity <= 7.5:
            sensitivity = round(args.sensitivity, 1)
            print(f"WARNING: the run mode \'{runMode}\' will be overwritten by the custom MMseqs sensitivity value of {args.sensitivity}.")
            # update the run mode accordingly
            runMode = "custom{:s}".format("".join(str(args.sensitivity).split(".", 1)))
            print(f"Run mode set to \'{runMode}\' (MMseqs2 sensitivity={args.sensitivity:.2f})\n")
        else:
            sys.stderr.write('\nERROR: the sensitivity parameter must have a value between 1.0 and 7.5\n')
            sys.exit(-6)

    # set the maximum length difference allowed if difference from default
    if args.max_len_diff != 0.5:
        if not (0. <= args.max_len_diff <= 1.0):
            sys.stderr.write('\nERROR: the length difference ratio must have a value between 0 and 1.\n')
            sys.exit(-6)
    # set the variable to control the creation of orthologous pairs
    output_relations = args.output_pairs
    if args.qfo_2011:
        output_relations = True
    # set the variable for MMseqs2 database indexing
    idx_dbs = True
    if args.no_indexing:
        idx_dbs = False

    # adjust the number of threads if required
    newThreads: int = os.cpu_count()
    memPerCore: float = 0.
    if not args.force_all_threads:
        newThreads, memPerCore = check_hardware_settings(threads, minPerCoreMem, debug=debug)
        threads = newThreads
    else: # make sure that the requested threads is not higher than the available
        from psutil import virtual_memory, cpu_count
        if threads > newThreads:
            sys.stderr.write(f"\nWARNING: the number of requested threads ({threads}) is higher than the available ({newThreads})")
            sys.stderr.write(f"\nThe number of threads will be set to {newThreads}")
            threads = newThreads
        # now compute the memory per thread
        availMem: float = round(virtual_memory().total / 1073741824., 2)
        memPerCore = round(availMem / threads, 2)
    del newThreads

    # directory with header and species names mapping
    runID = set_project_id(rId=args.project_id, runsDir=runsDir, args=args, debug=debug)
    runDir = os.path.join(runsDir, runID)
    # Will contains auxiliary files, like the prediction matrixes or pckl files
    auxDir = os.path.join(runDir, "aux/")
    systools.makedir(auxDir)
    # Pair-wise tables directory
    tblDir = os.path.join(runDir, "pairwise_orthologs/")
    systools.makedir(tblDir)
    # Directory with ortholog groups
    multiOutDir = os.path.join(runDir, 'ortholog_groups/')
    systools.makedir(multiOutDir)
    # variable ued in the update of input files
    updateInputNames = args.update_input_names
    removeOldSpecies = args.remove_old_species
    # name for multispecies groups
    multiSpeciesClstrNameAll = 'ortholog_groups.tsv'

    # set the MCL inflation rate
    inflation: float = args.inflation
    if (inflation < 1.2) or (inflation > 5):
        sys.stderr.write("\nWARNING: The inflation rate parameter must be between 1.2 and 5.0 while it was set to {:.2f}\n".format(inflation))
        sys.stderr.write("It will be automatically set to 1.5\n")
        inflation = 1.5

    # Set the prefilter matrix for MMseqs prefilter
    # pmtx:str = args.prefilter_mtx
    pmtx:str = "vtml80"

    print(f"\nRun START:\t{str(time.asctime(time.localtime(time.time())))}")
    print(f"SonicParanoid {softVersion} will be executed with the following parameters:")
    print(f"Run ID:\t{runID}")
    print(f"Run directory: {runDir}")
    print(f"Input directory: {inDir}")
    print(f"Input proteomes:\t{len(inPaths)}")
    print(f"Output directory: {outDir}")
    print(f"Run mode:\t{runMode} (MMseqs2 s={sensitivity})")
    print(f"Python version: {sys.version}")
    print(f"Python executables: {sys.executable}")
    print(f"SonicParanoid installation directory: {os.path.dirname(__file__)}")
    print(f"GCC version: {gccInfoTpl[1]}")
    print(f"GCC distribution: {gccInfoTpl[0]}")
    print(f"Alignments directory: {alignDir}")
    print(f"Pairwise tables directory: {tblDir}")
    print(f"Directory with ortholog groups: {multiOutDir}")
    print(f"Pairwise tables database directory: {pairwiseDbDir}")
    print(f"Update run:\t{str(update_run)}")
    print(f"Create pre-filter indexes:\t{str(idx_dbs)}")
    print(f"Complete overwrite:\t{overwrite}")
    print(f"Re-create ortholog tables:\t{owOrthoTbls}")
    print(f"Threads:\t{threads}")
    print(f"Memory per thread (Gigabytes):\t{memPerCore:.2f}")
    print(f"Minimum memory per thread (Gigabytes):\t{minPerCoreMem:.2f}")
    print(f"Prefilter matrix:\t{pmtx}")
    print(f"Compress alignments:\t{not(noCompress)}")
    if not noCompress:
        print(f"Compression level:\t{complev}")
    if not args.single_linkage:
        print(f"MCL inflation:\t{inflation:.2f}")

    # Populate the info dictionary
    infoDict["Version"] = softVersion
    infoDict["Date:"] = time.asctime(time.localtime(time.time()))
    infoDict["Run ID:"] = runID
    infoDict["Run directory:"] = runDir
    infoDict["Input directory:"] = inDir
    infoDict["Input proteomes:"] = str(len(inPaths))
    infoDict["Output directory:"] = outDir
    infoDict["MMseqs sensitivity:"] = str(sensitivity)
    infoDict["Python version:"] = sys.version
    infoDict["Python executables:"] = sys.executable
    infoDict["SonicParanoid installation:"] = os.path.dirname(__file__)
    infoDict["GCC version:"] = gccInfoTpl[1]
    infoDict["GCC distribution:"] = gccInfoTpl[0]
    infoDict["MMseqs DB directory:"] = str(dbDirectory)
    infoDict["Skip MMseqs DB indexing:"] = str(args.no_indexing)
    infoDict["Alignment directory:"] = str(alignDir)
    infoDict["Pairwise tables DB directory:"] = str(pairwiseDbDir)
    infoDict["Directory with pairwise orthologs:"] = str(tblDir)
    infoDict["Directory with ortholog groups:"] = str(multiOutDir)
    infoDict["Threads:"] = str(threads)
    infoDict["Memory per threads (Gigabytes):"] = str(memPerCore)
    infoDict["Minimum memory per threads (Gigabytes):"] = str(minPerCoreMem)
    infoDict["Update run:"] = str(update_run)
    infoDict["MMseqs prefilter matrix:"] = pmtx
    infoDict["Complete alignments:"] = str(complete_aln)
    infoDict["Max length difference for in-paralogs:"] = str(args.max_len_diff)
    infoDict["Overwrite pair-wise ortholog tables:"] = str(args.overwrite_tables)
    infoDict["Complete overwrite:"] = str(args.overwrite)
    infoDict["Skip creation of ortholog groups:"] = str(args.skip_multi_species)
    infoDict["Compress alignments:"] = str(not noCompress)
    if not noCompress:
        infoDict["Compression level:"] = str(complev)
    else:
        infoDict["Compression level:"] = "0"
    if not args.single_linkage:
        infoDict["MCL inflation:"] = str(args.inflation)
    if debug:
        infoDict["Directory with SonicParanoid runs:"] = str(runsDir)
        if args.single_linkage:
            infoDict["Maximum gene per species in groups:"] = str(args.max_gene_per_sp)
        infoDict["QfO 2011 run:"] = str(args.qfo_2011)
    # Check if the run already exists
    spFile = pairsFile = None

    # New run
    if not update_run:
        if debug:
            print("First run!")
        # write the file with information on the first run
        infoFile = write_run_info_file(runDir, infoDict, debug)
        copy(infoFile, os.path.join(infoDict["Output directory:"], "last_run_info.txt"))

        # Compute digests
        digestDict, repeatedFiles = idmapper.compute_hash_parallel(inPaths, algo=hashAlgo, bits=hashBits, threads=threads, debug=debug)
        spFile, mappedInputDir, mappedInPaths = idmapper.map_hdrs_parallel(inPaths, outDir=auxDir, digestDict=digestDict, idMapDict={}, threads=threads, debug=debug)
        del mappedInputDir
        del digestDict
        del repeatedFiles
        # create the snapshot file
        copy(spFile, snapshotFile)
        # predict pairwise orthology
        spFile, pairsFile, requiredPairsDict = orthodetect.run_sonicparanoid2_multiproc_essentials(mappedInPaths, outDir=runDir, tblDir=pairwiseDbDir, threads=threads, alignDir=alignDir, mmseqsDbDir=dbDirectory, create_idx=idx_dbs, sensitivity=sensitivity, cutoff=coff, confCutoff=0.05, pmtx=pmtx, lenDiffThr=args.max_len_diff, overwrite_all=overwrite, overwrite_tbls=owOrthoTbls, update_run=update_run, keepAlign=args.keep_raw_alignments, essentialMode=not(complete_aln), compress=not(noCompress), complev=complev, debug=debug)
        # remap the pairwise relations
        remap.remap_pairwise_relations_parallel(pairsFile, runDir=runDir, orthoDbDir=pairwiseDbDir, threads=threads, debug=debug)
        gc.collect()
        # sys.exit("DEBUG@sonicparanoid: [FIRST RUN] after remap.remap_pairwise_relations_parallel")

    # Update Run
    else:
        if debug:
            print("Update run!")
        # update the run info
        spFile, mappedInputDir, mappedInPaths = idmapper.update_run_info(inPaths=inPaths, outDir=auxDir, oldSpFile=snapshotFile, algo="sha256", bits=256, threads=threads,  updateNames=updateInputNames, removeOld=removeOldSpecies, overwrite=(overwrite or owOrthoTbls), debug=debug)
        # perfom the sanity check
        sanity_check(infoDict, debug)
        # write the file with information on the update run
        infoFile = write_run_info_file(runDir, infoDict, debug)
        # update info file for the last run
        copy(infoFile, os.path.join(infoDict["Output directory:"], "last_run_info.txt"))

        # sys.exit("DEBUG@sonicparanoid: [RUN_UPDATE] after remap.remap_pairwise_relations_parallel")

        # remove obsolete results
        # perform alignments and predict orthologs
        spFile, pairsFile, requiredPairsDict = orthodetect.run_sonicparanoid2_multiproc_essentials(mappedInPaths, outDir=runDir, tblDir=pairwiseDbDir, threads=threads, alignDir=alignDir, mmseqsDbDir=dbDirectory, create_idx=idx_dbs, sensitivity=sensitivity, cutoff=coff, confCutoff=0.05, pmtx=pmtx, lenDiffThr=args.max_len_diff, overwrite_all=overwrite, overwrite_tbls=owOrthoTbls, update_run=update_run, keepAlign=args.keep_raw_alignments, essentialMode=not(complete_aln), compress=not(noCompress), complev=complev, debug=debug)
        # remap the pairwise relations
        remap.remap_pairwise_relations_parallel(pairsFile, runDir=runDir, orthoDbDir=pairwiseDbDir, threads=threads, debug=debug)

    # infer ortholog groups
    if not skipMulti:
        if len(inPaths) > 2:
            if slc: # use QuickParanoid
                infer_orthogroups_qp(orthoDbDir=pairwiseDbDir, outDir=multiOutDir, sharedDir=runDir,sqlTblDir=multiOutDir, outName=multiSpeciesClstrNameAll, pairsList=requiredPairsDict,maxGenePerSp=maxGenePerSp, threads=threads, debug=debug)
            else: # use MCL
                infer_orthogroups_mcl(orthoDbDir=pairwiseDbDir, outDir=multiOutDir, sharedDir=runDir,sqlTblDir=multiOutDir, outName=multiSpeciesClstrNameAll, pairsList=requiredPairsDict,inflation=inflation, maxGenePerSp=maxGenePerSp, threads=threads, debug=debug)
        elif len(inPaths) == 2:
            infer_orthogroups_2_proteomes(orthoDbDir=pairwiseDbDir, outDir=multiOutDir,sharedDir=runDir, outName=multiSpeciesClstrNameAll, pairsList=requiredPairsDict,debug=debug)

    # remap species pairs file
    # load the mapping info
    id2SpDict, new2oldHdrDict = idmapper.load_mapping_dictionaries(runDir=auxDir, debug=debug)
    del new2oldHdrDict
    # create the pairs file with the original species names
    pairsFileRemapped = os.path.join(auxDir, "species_pairs_remapped.txt")
    with open(pairsFileRemapped, "w") as ofd:
        with open(pairsFile, "r") as ifd:
            for ln in ifd:
                sp1, sp2 = ln[:-1].split("-", 1)
                ofd.write(f"{id2SpDict[sp1]}-{id2SpDict[sp2]}\n")


    # generate file with pairwise relations
    if output_relations:
        # output directory for ortholog realtions
        relDict = os.path.join(runDir, "ortholog_relations")
        systools.makedir(relDict)
        # ALL
        orthoRelName = f"ortholog_pairs.{runID}.tsv"
        if args.qfo_2011:
            orthoRelName = f"ortholog_pairs_benchmark_qfo11.{runID}.tsv"
        # Extract pairs
        orthodetect.extract_ortholog_pairs(rootDir=os.path.join(runDir, "pairwise_orthologs"), outDir=relDict, outName=orthoRelName, pairsFile=pairsFileRemapped, coreOnly=False, singleDir=False, tblPrefix="", splitMode=args.qfo_2011, debug=debug)

    ex_end = round(time.perf_counter() - ex_start, 3)
    sys.stdout.write('\nTotal elapsed time (seconds):\t{:0.3f}\n'.format(ex_end))

    # remove Aux files (mapped input files and job matrixes)
    rmtree(os.path.join(runDir, "aux"))
    # cleanup MMseqs2 DB files
    if os.path.isdir(dbDirectory):
        rmtree(dbDirectory)
    # remove matrix files
    mtxDir = os.path.join(pairwiseDbDir, "matrixes")
    if os.path.isdir(mtxDir):
        # remove all its content
        rmtree(mtxDir)



if __name__ == "__main__":
    main()
