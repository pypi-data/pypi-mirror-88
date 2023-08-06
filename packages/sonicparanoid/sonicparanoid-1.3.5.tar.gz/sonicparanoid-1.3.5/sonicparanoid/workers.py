"""
 Contains function that will process queued jobs, among which alignments,
 and orthology inference.
"""

import os
import sys
import time
import subprocess
import multiprocessing as mp
import queue
import gc
import shutil
from filetype import is_archive
from typing import Dict, List, Any, Tuple

from sonicparanoid import inpyranoid
from sonicparanoid import sys_tools as systools
from sonicparanoid import colored_output as colout
from sonicparanoid import essentials_c as essentials
from sonicparanoid import mmseqs_parser_c as parser
from sonicparanoid import archiver



__module_name__ = "Workers"
__source__ = "workers.py"
__author__ = "Salvatore Cosentino"
__license__ = "GPL"
__version__ = "2.2"
__maintainer__ = "Cosentino Salvatore"
__email__ = "salvo981@gmail.com"



def info():
    """
    Contains functions that will process queued jobs
    """
    print("MODULE NAME:\t%s"%__module_name__)
    print("SOURCE FILE NAME:\t%s"%__source__)
    print("MODULE VERSION:\t%s"%__version__)
    print("LICENSE:\t%s"%__license__)
    print("AUTHOR:\t%s"%__author__)
    print("EMAIL:\t%s"%__email__)



def check_storage_for_mmseqs_dbs(outDir, reqSp=2, gbPerSpecies=0.95, debug=False):
    """Check that there is enough storage for the MMseqs2 index files."""
    if debug:
        print('\ncheck_storage_for_mmseqs_dbs :: START')
        print('Output directory: {:s}'.format(outDir))
        print('Number of databases to be created: {:d}'.format(reqSp))
        print('Required storage for index files: {:0.2f} gigabytes'.format(reqSp * gbPerSpecies))
    availSpaceGb = round(shutil.disk_usage(outDir).free / 1024 ** 3, 2)
    requiredSpaceGb = round(reqSp * gbPerSpecies, 2)
    # set the output variable
    createIdxFiles = True
    if requiredSpaceGb >= availSpaceGb:
        createIdxFiles = False
        infoLn = '{:0.2f} gigabytes required to store the index files for MMseqs2.'.format(requiredSpaceGb)
        colout.colored_info(outLn=infoLn, lnType='i', debug=debug)
        infoLn = 'only {:0.2f} gigabytes avaliable, MMseqs2 index files will not be created.'.format(availSpaceGb)
        colout.colored_info(outLn=infoLn, lnType='w', debug=debug)
        print('Please consider freeing some disk space to take advantage of MMseqs2 index files.')
    if debug:
        print('Available storage in your system (Gigabytes): {:0.2f}'.format(availSpaceGb))
    #sys.exit('DEBUG :: check_storage_for_mmseqs_dbs')
    # return the boolean
    return createIdxFiles



def create_dbs_parallel(jobs_queue, results_queue, inDir, dbDir, create_idx=True):
    """Create a a mmseqs2 database for the species in input dir."""
    while True:
        current_sp = jobs_queue.get(True, 1)
        if current_sp is None:
            break
        # check the query db name
        #queryDBname = os.path.basename(inFasta)
        inQueryPath = os.path.join(inDir, current_sp)
        if not os.path.isfile(inQueryPath):
            sys.stderr.write("ERROR: the input FASTA file \n{:s}\n was not found\n".format(inQueryPath))
            sys.exit(-2)
        queryDBname = "{:s}.mmseqs2db".format(current_sp)
        queryDBpath = "{:s}{:s}".format(dbDir, queryDBname)
        # create the database if does not exist yet
        if not os.path.isfile(queryDBpath):
            start_time = time.perf_counter()
            mmseqs_createdb(inQueryPath, outDir=dbDir, dbType=1, debug=False)
            if create_idx:
                mmseqs_createindex(queryDBpath, threads=2, debug=False)
            end_time = time.perf_counter()
            # add the execution time to the results queue
            results_queue.put((current_sp, str(round(end_time - start_time, 2))))



def consume_mmseqs_search_1cpu(jobs_queue, results_queue, inDir, dbDir, runDir, outDir, keepAlign, sensitivity, cutoff, pPath):
    while True:
        current_pair = jobs_queue.get(True, 1)
        if current_pair is None:
            break
        # extract input paths
        sp1, sp2 = current_pair.split("-", 1)
        inSeq = os.path.join(inDir, sp1)
        dbSeq = os.path.join(inDir, sp2)
        # create temporary directory name
        tmpMMseqsDirName = "tmp_{:s}-{:s}".format(sp1, sp2)
        # it MUST use 1 CPU
        parsedOutput, search_time, convert_time, parse_time, tot_time = mmseqs_1pass(inSeq, dbSeq, dbDir=dbDir, runDir=runDir, outDir=outDir, tmpDirName=tmpMMseqsDirName, keepAlign=keepAlign, sensitivity=sensitivity, evalue=1000, cutoff=cutoff, threads=1, pythonPath=pPath, debug=False)
        del tot_time
        # exit if the BLAST formatted file generation was not successful
        if not os.path.isfile(parsedOutput):
            sys.stderr.write("\nERROR: the MMseqs2 raw alignments could not be converted into the BLAST format.\n")
            sys.exit(-2)
        # store the execution time in the queue
        results_queue.put((current_pair, search_time, convert_time, parse_time))



def consume_alignment_jobs(jobs_queue, results_queue, runDir:str, dbDir:str, alnDir:str, keepAln:bool, sensitivity:float, cutoff:float, pmtx:str, compress:bool, complev:int) -> None:
    """
    Perform essential or complete alignments for a pair of proteomes.
    Only one complete alignment is performed if it is intra-proteome alignment.
    """
    while True:
        current_input = jobs_queue.get(True, 1)
        if current_input is None:
            break
        # extract job information
        pairTpl: Tuple[str, str] = ("", "")
        cntA: int = 0
        cntB: int = 0
        auxDir: str = os.path.join(runDir, "aux")
        inputSeqInfoDir: str = os.path.join(auxDir, "input_seq_info") 
        inDir: str = os.path.join(auxDir, "mapped_input")
        jobType: int = -1
        threads: int = 1
        pairTpl, jobType, threads, cntA, cntB = current_input
        tmpA: str = ""
        tmpB: str = ""
        tmpA, tmpB = pairTpl
        pair: str = f"{tmpA}-{tmpB}"
        invPair: str = f"{tmpB}-{tmpA}"
        pairAlnDir: str = ""
        # debug should be set only internally and should not be passed as a parameter
        debug: bool = False

        # will contain the results from the alignment job
        resList: List[Tuple[str, float, float, float, float, float]] = []
        # Given the pair A-B execute the alignments based on the following values
        # 0 -> A-B
        # 1 -> B-A only (essentials)
        # 2 -> A-B and B-A (essentials)
        # 3 -> B-A only (complete)
        # 4 -> A-B and B-A (complete)
        # execute the job based on the job type
        if (jobType == 0) or (jobType == 2) or (jobType == 4): # The first complete alignment
            if debug:
                print(f"\nComplete (FASTEST) alignment for pair {pair}")
            # create main directories and paths
            pairAlnDir: str = os.path.join(alnDir, tmpA)
            systools.makedir(pairAlnDir)
            inSeq = os.path.join(inDir, tmpA)
            dbSeq = os.path.join(inDir, tmpB)
            # define the for the temporary directory
            tmpMMseqsDirName = f"tmp_{pair}"
            # perfom the complete alignment
            # parsedOutput, search_time, convert_time, parse_time, tot_time = mmseqs_1pass(inSeq, dbSeq, dbDir=dbDir, runDir=runDir, outDir=alnDir, tmpDirName=tmpMMseqsDirName, keepAlign=keepAln, sensitivity=sensitivity, evalue=1000, cutoff=cutoff, pmtx=pmtx, threads=threads, debug=True)
            parsedOutput, search_time, convert_time, parse_time, tot_time = mmseqs_1pass(inSeq, dbSeq, dbDir=dbDir, runDir=inputSeqInfoDir, outDir=pairAlnDir, tmpDirName=tmpMMseqsDirName, keepAlign=keepAln, sensitivity=sensitivity, evalue=1000, cutoff=cutoff, pmtx=pmtx, compress=compress, complev=complev, threads=threads, debug=False)
            del tot_time
            # exit if the BLAST formatted file generation was not successful
            if not os.path.isfile(parsedOutput):
                sys.stderr.write(f"\nERROR: the MMseqs2 raw alignments for {pair} could not be converted into the BLAST format.\n")
                sys.exit(-2)
            # add execution times to the output list
            resList.append((pair, search_time, convert_time, parse_time, 100., 100., 0.))
            # sys.exit("DEBUG: @workers.consume_alignment_jobs. FIRST_COMPLETE_ALN")

        # perform the essential alignments if required
        if (jobType == 3) or (jobType == 4): # Complete alignments
            if debug:
                print(f"Complete alignment for pair {invPair}")
            # create main directories and paths
            # pairAlnDir: str = os.path.join(alnDir, invPair)
            pairAlnDir: str = os.path.join(alnDir, tmpB)
            systools.makedir(pairAlnDir)
            inSeq = os.path.join(inDir, tmpB)
            dbSeq = os.path.join(inDir, tmpA)
            # define the for the temporary directory
            tmpMMseqsDirName = f"tmp_{invPair}"
            # perfom the complete alignment
            parsedOutput, search_time, convert_time, parse_time, tot_time = mmseqs_1pass(inSeq, dbSeq, dbDir=dbDir, runDir=inputSeqInfoDir, outDir=pairAlnDir, tmpDirName=tmpMMseqsDirName, keepAlign=keepAln, sensitivity=sensitivity, evalue=1000, cutoff=cutoff, pmtx=pmtx, compress=compress, complev=complev, threads=threads, debug=False)
            del tot_time
            # exit if the BLAST formatted file generation was not successful
            if not os.path.isfile(parsedOutput):
                sys.stderr.write(f"\nERROR: the MMseqs2 raw alignments for {invPair} could not be converted into the BLAST format.\n")
                sys.exit(-2)
            # add execution times to the output list
            resList.append((invPair, search_time, convert_time, parse_time, 100., 100., 0.))
            # sys.exit("DEBUG: @workers.consume_alignment_jobs. COMPLETE_ALN")
        elif (jobType == 1) or (jobType == 2): # Essential alignments
            if debug:
                print(f"Essential alignment for pair {invPair}")
            reductionDict: Dict[int, List[str]] = {}
            # output directory for the single run
            pairAlnDir: str = os.path.join(alnDir, tmpB)
            essentialFaDir: str = os.path.join(pairAlnDir, invPair)
            refAlnDir: str = os.path.join(alnDir, tmpA)
            systools.makedir(pairAlnDir)
            systools.makedir(essentialFaDir)
            # tmpDir: str = os.path.join(runDir, "mapped_input")
            tmpPathAB: str = os.path.join(refAlnDir, f"{tmpA}-{tmpB}")
            # if the reference alignment does not exist yet
            if not os.path.isfile(tmpPathAB):
                sys.stderr.write(f"\nERROR: the reference alignment for pair {os.path.basename(tmpPathAB)} does not exist.")
                sys.stderr.write(f"\nYou must create the alignment for {pair} before aligning the pair {invPair}.")
                sys.exit(-7)
                results_queue.put((pair, 0., 0., 0., 0., 0., 0.))
                continue
            # start timer for reduction files creation
            reductionTime: float = time.perf_counter()
            # create the subsets
            # Use different functions if the alignment files are compressed
            if compress:
                reductionDict, pctB, pctA = essentials.create_essential_stacks_from_archive(tmpPathAB, cntA, cntB, debug=False)
            else:
                reductionDict, pctB, pctA = essentials.create_essential_stacks(tmpPathAB, cntA, cntB, debug=False)
            del tmpPathAB
            # extract sequences for A
            fastaPath: str = os.path.join(inDir, tmpA)
            reducedAPath: str = os.path.join(essentialFaDir, tmpA)
            essentials.extract_essential_proteins(fastaPath, reductionDict[int(tmpA)], reducedAPath, debug=False)
            # extract sequences for B
            fastaPath = os.path.join(inDir, tmpB)
            reducedBPath: str = os.path.join(essentialFaDir, tmpB)
            essentials.extract_essential_proteins(fastaPath, reductionDict[int(tmpB)], reducedBPath, debug=False)
            # create mmseqs database files
            mmseqs_createdb(reducedBPath, outDir=essentialFaDir, debug=False)
            mmseqs_createdb(reducedAPath, outDir=essentialFaDir, debug=False)[-1]
            reductionTime = round(time.perf_counter() - reductionTime, 3)
            # create temporary directory name
            tmpMMseqsDirName = f"tmp_{invPair}"
            # perform the alignments
            parsedOutput, search_time, convert_time, parse_time, tot_time = mmseqs_1pass(reducedBPath, reducedAPath, dbDir=essentialFaDir, runDir=essentialFaDir, outDir=pairAlnDir, tmpDirName=tmpMMseqsDirName, keepAlign=keepAln, sensitivity=sensitivity, evalue=1000, cutoff=cutoff, pmtx=pmtx, compress=compress, complev=complev, threads=threads, debug=False)
            # add execution times to the output list
            resList.append((invPair, search_time, convert_time, parse_time, pctA, pctB, reductionTime))
            # sys.exit("DEBUG: @workers.consume_alignment_jobs. ESSENTIAL_ALN")

        # add the results in the output queue
        results_queue.put(resList)



def consume_compress_jobs(jobs_queue, complev:int, removeSrc:bool):
    """Compress a file."""
    while True:
        current_paths = jobs_queue.get(True, 1)
        if current_paths is None:
            break
        # srcpath, outpath = current_paths
        archiver.compress_gzip(current_paths[0], current_paths[1], complev=complev, removeSrc=removeSrc, debug=False)



def consume_unarchive_jobs(jobs_queue, removeSrc:bool):
    """Extract archived file."""
    while True:
        current_paths = jobs_queue.get(True, 1)
        if current_paths is None:
            break
        # check the query db name
        archiver.extract_gzip(current_paths[0], current_paths[1], removeSrc=removeSrc, debug=False)



def consume_essential_alignments(jobs_queue, results_queue, runDir: str, alnDir: str, keepAln: bool, sensitivity: float, cutoff: float, pPath: str) -> None:
    """Perform single essential allignments."""
    while True:
        current_input = jobs_queue.get(True, 1)
        if current_input is None:
            break
        # extract job information
        pairTpl: Tuple[str, str] = ("", "")
        cntA: int = 0
        cntB: int = 0
        pairTpl, cntA, cntB = current_input
        tmpA: str = pairTpl[0]
        tmpB: str = pairTpl[1]
        reductionDict: Dict[int, List[str]] = {}

        # output directory for the single run
        pair: str = "{:s}-{:s}".format(tmpA, tmpB)
        pairAlnDir: str = os.path.join(alnDir, pair)
        systools.makedir(pairAlnDir)
        tmpDir: str = os.path.join(runDir, "mapped_input")
        tmpPathBA: str = os.path.join(alnDir, "{:s}-{:s}".format(tmpB, tmpA))
        # if the reference alignment does not exist yet
        if not os.path.isfile(tmpPathBA):
            sys.stderr.write("\nERROR: the reference alignment for pair {:s} does not exist.".format(os.path.basename(tmpPathBA)))
            sys.stderr.write("\nYou create the alignment for {:s} before aligning the pair {:s}.".format(os.path.basename(tmpPathBA), pair))
            results_queue.put((pair, 0., 0., 0., 0., 0., 0.))
            continue
        # start timer for reduction files creation
        reductionTime: float = time.perf_counter()
        # create the subsets
        reductionDict, pctB, pctA = essentials.create_essential_stacks(tmpPathBA, alnDir, cntB, cntA, debug=False)
        del tmpPathBA
        # extract sequences for A
        fastaPath: str = os.path.join(tmpDir, tmpA)
        reducedAPath: str = os.path.join(pairAlnDir, tmpA)
        essentials.extract_essential_proteins(fastaPath, reductionDict[int(tmpA)], reducedAPath, debug=False)
        # extract sequences for B
        fastaPath = os.path.join(tmpDir, tmpB)
        reducedBPath: str = os.path.join(pairAlnDir, tmpB)
        essentials.extract_essential_proteins(fastaPath, reductionDict[int(tmpB)], reducedBPath, debug=False)
        # create mmseqs database files
        mmseqs_createdb(reducedAPath, outDir=pairAlnDir, debug=False)
        dbPathB: str = mmseqs_createdb(reducedBPath, outDir=pairAlnDir, debug=False)[-1]
        mmseqs_createindex(dbPathB, debug=False)
        # end time for reduction files creation creation
        reductionTime = round(time.perf_counter() - reductionTime, 3)
        # create temporary directory name
        tmpMMseqsDirName = 'tmp_{:s}'.format(pair)
        # perform the alignments
        parsedOutput, search_time, convert_time, parse_time, tot_time = mmseqs_1pass(reducedAPath, reducedBPath, dbDir=pairAlnDir, runDir=pairAlnDir, outDir=alnDir, tmpDirName=tmpMMseqsDirName, keepAlign=keepAln, sensitivity=sensitivity, evalue=1000, cutoff=cutoff, threads=1, pythonPath=pPath, debug=False)
        del parsedOutput, tot_time
        # add results to the queue
        results_queue.put((pair, search_time, convert_time, parse_time, pctA, pctB, reductionTime))



def consume_orthology_inference_sharedict(jobs_queue, results_queue, inDir, outDir=os.getcwd(), sharedDir=None, sharedWithinDict=None, cutoff=40, confCutoff=0.05, lenDiffThr=0.5, threads=8, compressed=False):
    """Perform orthology inference in parallel."""
    while True:
        current_pair = jobs_queue.get(True, 1)
        if current_pair is None:
            break
        # create the output directory if needed
        # prepare the run
        sp1, sp2 = current_pair.split("-", 1)
        runDir = os.path.join(outDir, f"{sp1}/{current_pair}")
        systools.makedir(runDir)
        inSp1 = os.path.join(inDir, sp1)
        inSp2 = os.path.join(inDir, sp2)
        # check that the input files do exist
        if not os.path.isfile(inSp1):
            sys.stderr.write(f"ERROR: The input file for {sp1} was not found, please provide a valid path")
            sys.exit(-2)
        if not os.path.isfile(inSp2):
            sys.stderr.write(f"ERROR: The input file for {sp2} was not found, please provide a valid path")
            sys.exit(-2)
        # AB
        AB = f"{sp1}-{sp2}"
        shPathAB = os.path.join(sharedDir, f"{sp1}/{AB}")
        if not os.path.isfile(shPathAB):
            sys.stderr.write(f"ERROR: The alignment file for {AB} was not found, please generate the alignments first.\n")
            sys.exit(-2)
        # BA
        BA = f"{sp2}-{sp1}"
        shPathBA = os.path.join(sharedDir, f"{sp2}/{BA}")
        if not os.path.isfile(shPathBA):
            sys.stderr.write(f"ERROR: The alignment file for {BA} was not found, please generate the alignments first.\n")
            sys.exit(-2)

        # prepare paths for output tables
        outTable = os.path.join(runDir, f"table.{current_pair}")
        # infer orthologs
        # use perf_counter (includes time spent during sleep)
        orthology_prediction_start = time.perf_counter()
        # Perfom the prediction
        inpyranoid.infer_orthologs_shared_dict(inSp1, inSp2, alignDir=sharedDir, outDir=runDir, sharedWithinDict=sharedWithinDict, confCutoff=confCutoff, lenDiffThr=lenDiffThr, compressed=compressed, debug=False)
        #check that all the files have been created
        if not os.path.isfile(outTable):
            sys.stderr.write(f"WARNING: the ortholog table file {outTable} was not generated.")
            outTable = None
        #everything went ok!
        end_time = time.perf_counter()
        orthology_prediction_tot = round(end_time - orthology_prediction_start, 2)
        # add the execution time to the results queue
        results_queue.put((current_pair, str(orthology_prediction_tot)))

        # Debug should only be set manually
        debug:bool = False
        if debug:
            sys.stdout.write(f"\nOrthology prediction {current_pair} (seconds):\t{orthology_prediction_tot}\n")
        # sys.exit("DEBUG :: workers :: consume_orthology_inference_sharedict :: final part")



# DEBUG-FUNCTION: this should be removed in future releases
'''
def consume_orthology_inference(jobs_queue, results_queue, inDir, outDir=os.getcwd(), sharedDir=None, cutoff=40, confCutoff=0.05, lenDiffThr=0.5, threads=8, debug=False):
    """Perform orthology inference in parallel."""
    while True:
        current_pair = jobs_queue.get(True, 1)
        if current_pair is None:
            break
        # create the output directory iof needed
        # prepare the run
        sp1, sp2 = current_pair.split('-', 1)
        runDir = os.path.join(outDir, current_pair)
        systools.makedir(runDir)
        inSp1 = os.path.join(inDir, sp1)
        inSp2 = os.path.join(inDir, sp2)
        # check that the input files do exist
        if not os.path.isfile(inSp1):
            sys.stderr.write("ERROR: The input file for {:s} was not found, please provide a valid path.\n".format(sp1))
            sys.exit(-2)
        if not os.path.isfile(inSp2):
            sys.stderr.write("ERROR: The input file for {:s} was not found, please provide a valid path.\n".format(sp2))
            sys.exit(-2)
        # prepare the names of the required alignments
        # copy AA
        AA = '{:s}-{:s}'.format(sp1, sp1)
        shPathAA = os.path.join(sharedDir, AA)
        if not os.path.isfile(shPathAA):
            sys.stderr.write("ERROR: The alignment file for {:s} was not found, please generate the alignments first.\n".format(AA))
            sys.exit(-2)
        # copy BB
        BB = '{:s}-{:s}'.format(sp2, sp2)
        shPathBB = os.path.join(sharedDir, BB)
        if not os.path.isfile(shPathBB):
            sys.stderr.write("ERROR: The alignment file for {:s} was not found, please generate the alignments first.\n".format(BB))
            sys.exit(-2)
        # copy AB
        AB = '{:s}-{:s}'.format(sp1, sp2)
        shPathAB = os.path.join(sharedDir, AB)
        if not os.path.isfile(shPathAB):
            sys.stderr.write("ERROR: The alignment file for {:s} was not found, please generate the alignments first.\n".format(AB))
            sys.exit(-2)
        # copy BA
        BA = '{:s}-{:s}'.format(sp2, sp1)
        shPathBA = os.path.join(sharedDir, BA)
        if not os.path.isfile(shPathBA):
            sys.stderr.write("ERROR: The alignment file for {:s} was not found, please generate the alignments first.\n".format(BA))
            sys.exit(-2)
        #sys.exit('DEBUG :: workers :: consume_orthology_inference_jobs :: after files copy')

        # prepare paths for output tables
        outTable = os.path.join(runDir, 'table.{:s}'.format(current_pair))

        # infer orthologs
        # use perf_counter (includes time spent during sleep)
        orthology_prediction_start = time.perf_counter()
        inpyranoid.infer_orthologs(inSp1, inSp2, alignDir=sharedDir, outDir=runDir, confCutoff=confCutoff, lenDiffThr=lenDiffThr, debug=False)
        #check that all the files have been created
        if not os.path.isfile(outTable):
            sys.stderr.write('WARNING: the ortholog table file %s was not generated.'%outTable)
            outTable = None
        #everything went ok!
        # use perf_counter (includes time spent during sleep)
        end_time = time.perf_counter()
        orthology_prediction_tot = round(end_time - orthology_prediction_start, 2)
        # add the execution time to the results queue
        results_queue.put((current_pair, str(orthology_prediction_tot)))
        if debug:
            sys.stdout.write('\nOrthology prediction {:s} (seconds):\t{:s}\n'.format(current_pair, str(orthology_prediction_tot)))
'''



def get_mmseqs_path():
    """Return the directory in which MMseqs2 binaries are stored."""
    #import platform
    mmseqsPath = None
    pySrcDir = os.path.dirname(os.path.abspath(__file__))
    mmseqsPath = os.path.join(pySrcDir, 'bin/mmseqs')
    if not os.path.isfile(mmseqsPath):
        sys.stderr.write('\nERROR: mmseqs2 was not found, please install it and execute setup_sonicparanoid.py.')
        sys.exit(-5)
    # return the path
    return mmseqsPath



def mmseqs_1pass(inSeq, dbSeq, dbDir=os.getcwd(), runDir=os.getcwd(), outDir=os.getcwd(), tmpDirName=None, keepAlign=False, sensitivity=4.0, evalue=1000, cutoff=40, pmtx="blosum62", compress:bool=False, complev:int=5, threads:int=4, debug=False):
    """Execute the 1-pass alignment mmseqs2 similar to the one implemented in core-inparanoid."""
    if debug:
        print("\nmmseqs_1pass :: START")
        print(f"Input query FASTA file:\t{inSeq}")
        print(f"Input target FASTA file:\t{dbSeq}")
        print(f"mmseqs2 database directory:\t{dbDir}")
        print(f"Directory with run supplementary files: {runDir}")
        print(f"Output directory:\t{outDir}")
        print(f"MMseqs2 tmp directory:\t{tmpDirName}")
        print(f"Do not remove alignment files:\t{keepAlign}")
        print(f"MMseqs2 sensitivity (-s):\t{sensitivity}")
        print(f"Bitscore cutoff:\t{cutoff}")
        print(f"MMseqs2 prefilter substitution matrix:\t{pmtx}")
        print(f"Compress output:\t{compress}")
        print(f"Compression level:\t{complev}")
        print(f"Threads:\t{threads}")

    # create the directory in which the alignment will be performed
    pair: str = f"{os.path.basename(inSeq)}-{os.path.basename(dbSeq)}"
    pairAlnDir: str = os.path.join(outDir, pair)
    systools.makedir(pairAlnDir)

    #start the timing which will also include the time for the index, database creation (if required) and parsing
    # create mmseqs alignment conveted into blastp tab-separated format
    blastLikeOutput, search_time, convert_time = mmseqs_search(inSeq, dbSeq, dbDir=dbDir, outDir=pairAlnDir, tmpDirName=tmpDirName, sensitivity=sensitivity, pmtx=pmtx, evalue=1000, threads=threads, cleanUp=False, debug=debug)
    parserPath = os.path.join(outDir, "mmseqs_parser_cython.py")
    # check cutoff
    if cutoff < 30:
        sys.stderr.write(f"\nWARNING: the cutoff value ({cutoff}) is below 40, and will be set to 40.\n")
        cutoff = 40

    # start timing the parsing
    # use perf_counter (includes time spent during sleep)
    start_time = time.perf_counter()
    # prepare now the parsing
    # EXAMPLE: python3 mmseqs_parser_cython.py --input mmseqs2blast.A-B --query A --db B --output A-B --cutoff 40
    parsedOutput: str = blastLikeOutput.rsplit(".", 1)[-1]
    parsedOutput = os.path.join(pairAlnDir, parsedOutput)
    # parse Blast-like output
    parse_blast_output(blastLikeOutput, inSeq, dbSeq, parsedOutput, runDir, cutoff, compress, complev, debug)

    ''' TO REMOVE
    # READ LENGTHS OR HDRS FROM FILE
    parseCmd = f"{pythonPath} {parserPath} --input {blastLikeOutput} --query {inSeq} --db {dbSeq} --output {parsedOutput} --cutoff {cutoff} --run-dir {runDir}"
    if debug:
        print(f"Parse CMD:\n{parseCmd}")

    #execute the system call for parsing
    subprocess.run(parseCmd, shell=True)
    '''
    # use perf_time (includes time spent during sleep)
    parse_time = round(time.perf_counter() - start_time, 2)
    tot_time = round(search_time + convert_time + parse_time, 2)
    if debug:
        sys.stdout.write(f"\nMMseqs2 alignment and parsing elapsed time (seconds):\t{tot_time}\n")
    # Temporary final name
    tmpFinalPath: str = os.path.join(outDir, f"_{pair}")
    systools.copy(parsedOutput, tmpFinalPath)
    # remove the aligment directory if required
    if keepAlign:
        for r, d, files in os.walk(pairAlnDir):
            for name in files:
                tPath = os.path.join(r, name)
                if os.path.isfile(tPath) and name[0] == "m":
                    systools.move(tPath, outDir)
            break
    # remove directory content
    shutil.rmtree(pairAlnDir)
    parsedOutput = os.path.join(outDir, pair)
    os.rename(tmpFinalPath, parsedOutput)
    # reset original working directory
    # os.chdir(prevDir) # TO REMOVE
    return (parsedOutput, search_time, convert_time, parse_time, tot_time)



def mmseqs_createdb(inSeq:str, outDir:str=os.getcwd(), dbType:int=1, debug:bool=False):
    """Create a database file for mmseqs2 from the input sequence file."""
    if debug:
        print("mmseqs_createdb :: START")
        print("Input FASTA file:\t%s"%inSeq)
        print("Database type:\t%d"%dbType)
        print("Outdir:\t%s"%outDir)
    #check that the input file and the database exist
    if not os.path.isfile(inSeq):
        sys.stderr.write("The file %s was not found, please provide the path to a valid FASTA file."%inSeq)
        sys.exit(-2)
    #check if the database exists
    if outDir[-1] != "/":
        outDir += "/"
    # create dir if not already exists
    systools.makedir(outDir)
    # check the set db name
    dbName = os.path.basename(inSeq)
    dbName = dbName.split(".")[0] # take the left part of the file name
    dbName = "%s.mmseqs2db"%dbName
    dbPath = "%s%s"%(outDir, dbName)
    # command to be executed
    # EXAMPLE; mmseqs createdb in.fasta /outdir/mydb
    makeDbCmd = f"{get_mmseqs_path()} createdb {inSeq} {dbPath} -v 0"
    if debug:
        print(f"mmseqs2 createdb CMD:\n{makeDbCmd}")
    #execute the system call
    process = subprocess.Popen(makeDbCmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout_val, stderr_val = process.communicate() #get stdout and stderr
    process.wait()
    if debug:
        print("STDOUT:\n%s\n"%stdout_val)
        print("STDERR:\n%s\n"%stderr_val)
    #return a tuple with the results
    return(stdout_val, stderr_val, makeDbCmd, dbPath)



def mmseqs_createindex(dbPath:str, threads:int=2, debug:bool=False):
    """Create a index from a mmseq2 database file."""
    if debug:
        print("mmseqs_createindex :: START")
        print(f"Input mmseqs2 db file:\t{dbPath}")
        print(f"Threads:\t{threads}")
    #check that the database file exist
    if not os.path.isfile(dbPath):
        sys.stderr.write(f"The file {dbPath} was not found, please provide the path to a mmseqs2 database file")
        sys.exit(-2)
    # Prepare file names and commands
    tmpBname = os.path.basename(dbPath)
    tmpDir = "{:s}/tmp_{:s}/".format(os.path.dirname(dbPath), os.path.basename(tmpBname.split(".", 1)[0]))
    systools.makedir(tmpDir)
    # command to be executed
    # EXAMPLE; mmseqs createindex in.mmseqs2_db
    makeIdxCmd = f"{get_mmseqs_path()} createindex {dbPath} {tmpDir} --threads {threads} --search-type 1 -v 0"
    if debug:
        print(f"mmseqs2 createindex CMD:\n{makeIdxCmd}")
    #execute the system call
    process = subprocess.Popen(makeIdxCmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout_val, stderr_val = process.communicate() #get stdout and stderr
    process.wait()
    if debug:
        print(f"STDOUT:\n{stdout_val}\n")
        print(f"STDERR:\n{stderr_val}\n")
    # make sure that the 3 idx files have been properly created
    idx1: str = f"{dbPath}.idx"
    if not os.path.isfile(idx1):
        sys.stderr.write(f"The MMseqs2 index file {idx1} could not be created.")
        sys.exit(-2)
    idx2: str = f"{dbPath}.idx.index"
    if not os.path.isfile(idx2):
        sys.stderr.write(f"\nWARNING: The MMseqs2 index file {idx2} could not be created.")
        sys.exit(-2)
    # remove the temporary directory
    shutil.rmtree(path=tmpDir)
    # return a output tuple
    return(stdout_val, stderr_val, makeIdxCmd, idx1, idx2)



def mmseqs_search(inSeq, dbSeq, dbDir=os.getcwd(), outDir=os.getcwd(), tmpDirName=None, sensitivity=4.0, pmtx="blosum62", evalue=1000, threads=4, cleanUp=False, debug=False):
    """Align protein sequences using MMseqs2."""
    if debug:
        print("\nmmseqs_search :: START")
        print(f"Input query FASTA file: {inSeq}")
        print(f"Input target FASTA file: {dbSeq}")
        print(f"mmseqs2 database directory: {dbDir}")
        print(f"Output directory: {outDir}")
        print(f"MMseqs2 tmp directory:\t{tmpDirName}")
        print(f"MMseqs2 sensitivity (-s):\t{sensitivity}")
        print(f"MMseqs2 prefilter substitution matrix:\t{pmtx}")
        print(f"Threads:\t{threads}")
        print(f"Remove temporary files:\t{cleanUp}")
    #check that the input file and the database exist
    if not os.path.isfile(inSeq):
        sys.stderr.write(f"ERROR: The query file {inSeq}\nwas not found, please provide the path to a valid FASTA file")
        sys.exit(-2)
    if not os.path.isfile(dbSeq):
        sys.stderr.write(f"ERROR: The target file {dbSeq}\nwas not found, please provide the path to a valid FASTA file")
        sys.exit(-2)
    # check sensitivity
    if (sensitivity < 1) or sensitivity > 7.5:
        sys.stderr.write("\nERROR: the sensitivity value for MMseqs2 must be a value between 1.0 and 7.5.\n")
        sys.exit(-5)
    # create directory if not previously created
    systools.makedir(outDir)
    systools.makedir(dbDir)
    # set the tmp dir
    tmpDir = None
    if tmpDirName is None:
        tmpDir = os.path.join(outDir, "tmp_mmseqs")
    else:
        tmpDir = os.path.join(outDir, tmpDirName)
    systools.makedir(tmpDir)
    # check the query db name
    queryDBname = os.path.basename(inSeq)
    queryDBname = queryDBname.split(".")[0] # take the left part of the file name
    queryDBname = f"{queryDBname}.mmseqs2db"
    queryDBpath = os.path.join(dbDir, queryDBname)
    # create the database if does not exist yet
    if not os.path.isfile(queryDBpath):
        mmseqs_createdb(inSeq, outDir=dbDir, debug=debug)
        mmseqs_createindex(queryDBpath, threads=threads, debug=debug)
    # check the target db name
    targetDBname = os.path.basename(dbSeq)
    targetDBname = targetDBname.split(".")[0] # take the left part of the file name
    targetDBname = f"{targetDBname}.mmseqs2db"
    targetDBpath = os.path.join(dbDir, targetDBname)
    # create the database if does not exist yet
    if not os.path.isfile(targetDBpath):
        mmseqs_createdb(dbSeq, outDir=dbDir, debug=debug)
        mmseqs_createindex(targetDBpath, threads=threads, debug=debug)
    # set output name
    pairName = f"{os.path.basename(inSeq)}-{os.path.basename(dbSeq)}"
    rawOutName = f"mmseqs2raw.{pairName}"
    rawOutPath = os.path.join(outDir, rawOutName)
    blastOutName = f"mmseqs2blast.{pairName}"
    blastOutPath = os.path.join(outDir, blastOutName)
    # start measuring the execution time
    # use perf_counter (includes time spent during sleep)
    start_time = time.perf_counter()
    # command to be executed
    minUngappedScore = 15
    mtxSettings:str = "--seed-sub-mat nucl:nucleotide.out,aa:blosum62.out"
    if pmtx != "blosum62":
        mtxSettings = "" # just use the default for MMseqs2
    # EXAMPLE: mmseqs search queryDBfile targetDBfile outputFile tmpDir -s 7.5 -e 100000 --theads threads
    searchCmd: str = f"{get_mmseqs_path()} search {queryDBpath} {targetDBpath} {rawOutPath} {tmpDir} -s {str(sensitivity)} --threads {threads:d} -v 0 {mtxSettings} --min-ungapped-score {minUngappedScore} --alignment-mode 2 --alt-ali 10 --search-type 1"
    # This prevents MMseqs2 to crush when running at high sensitivity
    if sensitivity > 6:
        searchCmd = f"{searchCmd} --db-load-mode 3"
    if debug:
        print(f"mmseqs2 search CMD:\t{searchCmd}")
    # use run (or call)
    subprocess.run(searchCmd, shell=True)

    # output an error if the Alignment did not finish correctly
    if threads > 1: # multiple raw files are generated
        if not os.path.isfile(f"{rawOutPath}.0"):
            sys.stderr.write(f"\nERROR [mmseqs_search()]: the MMseqs2 raw alignment file\n{rawOutPath}\nwas not generated.\n")
            sys.exit(-2)
    else: # a single raw file is created
        if not os.path.isfile(rawOutPath):
            sys.stderr.write(f"\nERROR [mmseqs_search()]: the MMseqs2 raw alignment file\n{rawOutPath}\nwas not generated.\n")
            sys.exit(-2)

    # stop counter
    # use perf_counter (includes time spent during sleep)
    end_search = time.perf_counter()
    search_time = round(end_search - start_time, 2)
    # convert the output to tab-separated BLAST output
    # EXAMPLE: mmseqs convertalis query.db target.db query_target_rawout query_target_blastout
    # Only output specific files in the BLAST-formatted output
    # query,target,qstart,qend,tstart,tend,bits
    columns: str = "query,target,qstart,qend,tstart,tend,bits"
    convertCmd = f"{get_mmseqs_path()} convertalis {queryDBpath} {targetDBpath} {rawOutPath} {blastOutPath} -v 0 --format-mode 0 --search-type 1 --format-output {columns} --threads {threads:d}"

    # perform the file conversion
    subprocess.run(convertCmd, shell=True)
    if debug:
        print(f"mmseqs2 convertalis CMD:\n{convertCmd}")
    # exec time conversion
    # use perf_counter (includes time spent during sleep)
    convert_time = round(time.perf_counter() - end_search, 2)
    # output an error if the Alignment could not be converted
    if not os.path.isfile(blastOutPath):
        sys.stderr.write(f"\nERROR: the MMseqs2 raw alignments could not be converted into the BLAST format.\n{blastOutPath}\n")
        sys.exit(-2)
    return (blastOutPath, search_time, convert_time)



def parallel_archive_processing(paths:List[Tuple[str, str]], complev:int=5, removeSrc:bool=False, threads:int=4, compress:bool=True, debug:bool=False) -> None:
    """Compress input files in parallel."""
    if debug:
        print("\nparallel_archive_processing :: START")
        if compress:
            print(f"Files to be compressed:\t{len(paths)}")
            print(f"Compression level:\t{complev}")
        else:
            print(f"Archives to be decompressed:\t{len(paths)}")
        print(f"Remove original file:\t{removeSrc}")
        print(f"Threads:\t{threads}")
        print(f"Compress:\t{compress}")

    # create the queue and start adding jobs
    jobs_queue = mp.Queue(maxsize=len(paths) + threads)
    # fill the queue with the file paths
    for tpl in paths:
        jobs_queue.put(tpl)

    # add flags for ended jobs
    for i in range(0, threads):
        sys.stdout.flush()
        jobs_queue.put(None)

    # execute the jobs
    if compress:
        # perform the file compression
        runningJobs = [mp.Process(target=consume_compress_jobs, args=(jobs_queue, complev, removeSrc)) for i_ in range(threads)]
    else:
        # perform the file compression
        runningJobs = [mp.Process(target=consume_unarchive_jobs, args=(jobs_queue, removeSrc)) for i_ in range(threads)]

    # execute the jobs
    for proc in runningJobs:
        proc.start()

    # calculate cpu-time for compression
    processing_start = time.perf_counter()
    # write some message...
    if compress:
        sys.stdout.write(f"\nArchiving {len(paths)} files...please be patient...")
    else:
        sys.stdout.write(f"\nExtracting {len(paths)} archived files...please be patient...")

    # this joins the processes after we got the results
    for proc in runningJobs:
        while proc.is_alive():
            proc.join()

    # stop the counter for the alignment time
    if compress:
        sys.stdout.write(f"\nCompression of {len(paths)} files compression elapsed time (seconds):\t{round(time.perf_counter() - processing_start, 3)}\n")
    else:
        sys.stdout.write(f"\nExtraction of {len(paths)} archives elapsed time (seconds):\t{round(time.perf_counter() - processing_start, 3)}\n")



def parse_blast_output(inBlastOut:str, query:str, target:str, outPath:str, runDir:str, cutoff:int=40, compress:bool=False, complev:int=5, debug:bool=False):
    """Parse BLAST-like output file and generate SonicParanoid alignment file"""
    if debug:
        print("\nparse_blast_output :: START")
        print(f"BLAST output to be parsed: {inBlastOut}")
        print(f"Query: {query}")
        print(f"Target: {target}")
        print(f"Parsed output: {outPath}")
        print(f"Directory with accessory files: {runDir}")
        print(f"Bitscore cutoff:\t{cutoff}")
        print(f"Compress output:\t{compress}")
        if compress:
            print(f"Compression level:\t{complev}")

    outName:str = os.path.basename(outPath)
    outDir:str = os.path.dirname(outPath)
    bsName: str = os.path.basename(inBlastOut)
    # use pickle files
    qSeqLenPath:str = os.path.join(runDir, f"{os.path.basename(query)}.len.pckl")
    tSeqLenPath:str = os.path.join(runDir, f"{os.path.basename(target)}.len.pckl")

    ########## sort the BLAST output ###########
    # sort blast_output -k1,1 -k2,2 -k12nr > sorted_output
    sortPath: str = os.path.join(outDir, f"sorted_{bsName}")

    ##### RESTORE THIS IF REQUIRED #####
    # ofd = open(sortPath, "w")
    #sort(inBlastOut, '-k1,1', '-k2,2', '-k12nr', _out=ofd)
    # sort(inBlastOut, '-k1,1', '-k2,2', '-k7nr', _out=ofd)
    # ofd.close()
    ###################################

    sortCmd: str = f"sort -o {sortPath} -k1,1 -k2,2 -k7nr {inBlastOut}"
    # use run (or call)
    subprocess.run(sortCmd, shell=True)

    if debug:
        print(f"Sort CMD:\n{sortCmd}")

    if not os.path.isfile(inBlastOut):
        sys.stderr.write(f"WARNING: the file\n{inBlastOut}\nwas not found...")
    # remove the unsorted output and rename
    os.remove(inBlastOut)
    os.rename(sortPath, inBlastOut)
    ############################################

    # Parse the MMseqs2 output
    parser.mmseqs_parser_7flds(inBlastOut, qSeqLenPath, tSeqLenPath, outDir=outDir, outName=outName, scoreCoff=cutoff, compress=compress, complev=complev, debug=False)



def perform_parallel_dbs_creation(spList, inDir, dbDir, create_idx=True, threads=4, debug=False):
    """Create MMseqs2 databases in parallel"""
    # create the queue and start adding
    make_dbs_queue = mp.Queue(maxsize=len(spList) + threads)

    # fill the queue with the processes
    for sp in spList:
        sys.stdout.flush()
        make_dbs_queue.put(os.path.basename(sp))

    # add flags for completed jobs
    for i in range(0, threads):
        sys.stdout.flush()
        make_dbs_queue.put(None)

    # Queue to contain the execution time
    results_queue = mp.Queue(maxsize=len(spList))

    # call the method inside workers
    runningJobs = [mp.Process(target=create_dbs_parallel, args=(make_dbs_queue, results_queue, inDir, dbDir, create_idx)) for i_ in range(threads)]

    for proc in runningJobs:
        proc.start()

    while True:
        try:
            sp, tot_time = results_queue.get(False, 0.01)
            #ofd.write('{:s}\t{:s}\t{:s}\t{:s}\n'.format(p, str(s_time), str(c_time), str(p_time)))
            if debug:
                sys.stdout.write(f"{sp} database created:\t{tot_time}\n")
        except queue.Empty:
            pass
        allExited = True
        for t in runningJobs:
            if t.exitcode is None:
                allExited = False
                break
        if allExited & results_queue.empty():
            break

    # this joins the processes after we got the results
    for proc in runningJobs:
        while proc.is_alive():
            proc.join()



# DEBUG-FUNCTION: this should be removed in future releases
'''
def perform_mmseqs_multiproc_alignments(requiredAln, inDir, outDir, dbDir, runDir, create_idx=True, sensitivity=4., cutoff=40, threads=4, keepAlign=False, firstCicle: bool=True, debug=False):
    system_cpus = mp.cpu_count()
    # check threads count
    if threads > system_cpus:
        threads = system_cpus

    if debug:
        print("\nperform_mmseqs_multiproc_alignments :: START")
        print("Pairs to be aligned:\t{:d}".format(len(requiredAln)))
        print("Directory with input proteomes: {:s}".format(inDir))
        print("Output directory with alignment files: {:s}".format(outDir))
        print("Directory alignments MMseqs DB files: {:s}".format(dbDir))
        print("Directory with run supplementary files: {:s}".format(runDir))
        print("Create MMseqs index files:\t{:s}".format(str(create_idx)))
        print("Sensitivity:\t{:.2f}".format(sensitivity))
        print("Bitscore cutoff:\t{:d}".format(cutoff))
        print("Threads:\t{:d}".format(threads))
        print("Keep alignment files:\t{:s}".format(str(keepAlign)))
        print("First cicle of alignments:\t{:s}".format(str(firstCicle)))

    # create dictionary with species involved in alignments
    reqSpDict = {}
    for pair in requiredAln:
        sp1, sp2 = pair.split('-', 1)
        if not sp1 in reqSpDict:
            reqSpDict[sp1] = None
        if not sp2 in reqSpDict:
            reqSpDict[sp2] = None

    # Make sure there is enough storage to crate the index files
    # overwrites the create_idx variable
    if create_idx:
        create_idx = check_storage_for_mmseqs_dbs(outDir, reqSp=len(reqSpDict), gbPerSpecies=1, debug=debug)

    # create databases
    sys.stdout.write('\nCreating {:d} MMseqs2 databases...\n'.format(len(reqSpDict)))
    # timer for databases creation
    start_time: float = time.perf_counter()

    # create databases in parallel
    perform_parallel_dbs_creation(list(reqSpDict.keys()), inDir, dbDir, create_idx=create_idx, threads=threads, debug=debug)
    # end time for databases creation
    end_time: float = time.perf_counter()
    sys.stdout.write('\nMMseqs2 databases creation elapsed time (seconds):\t{:s}\n'.format(str(round(end_time - start_time, 3))))
    # delete timers
    del start_time, end_time
    # calculate cpu-time for alignments
    align_start: float = time.perf_counter()
    # find the mmseqs2 parser in the source directory
    pySrcDir = os.path.dirname(os.path.abspath(__file__))
    mmseqsparser: str = os.path.join(pySrcDir, 'mmseqs_parser_cython.py')
    # copy the file to the output directory
    systools.copy(mmseqsparser, outDir, metaData=False, debug=False)
    mmseqsparser = os.path.join(outDir, 'mmseqs_parser_cython.py')
    os.chmod(mmseqsparser, 0o751)
    # find and copy the parser module
    parserModuleFound: bool = False
    for el in os.listdir(pySrcDir):
        if el.startswith('mmseqs_parser_c'):
            if el.endswith('.pyx') or el.endswith('.c'):
                continue
            systools.copy(os.path.join(pySrcDir, el), outDir, metaData=False, debug=False)
            parserModuleFound = True
            break
    del parserModuleFound, pySrcDir

    # create the queue and start adding
    align_queue = mp.Queue(maxsize=len(requiredAln) + threads)

    # fill the queue with the processes
    for pair in requiredAln:
        sys.stdout.flush()
        align_queue.put(pair)
    # add flags for ended jobs
    for i in range(0, threads):
        sys.stdout.flush()
        align_queue.put(None)

    # Queue to contain the execution time
    results_queue = mp.Queue(maxsize=len(requiredAln))

    # get the path to python3 executable
    pythonPath = sys.executable
    # call the method inside workers
    runningJobs = [mp.Process(target=consume_mmseqs_search_1cpu, args=(align_queue, results_queue, inDir, dbDir, runDir, outDir, keepAlign, sensitivity, cutoff, pythonPath)) for i_ in range(threads)]

    # run the jobs
    for proc in runningJobs:
        proc.start()

    # open the file in which the time information will be stored
    # use the parent directory name of the database directory as suffix
    alnCicle: int = 1
    if not firstCicle:
        alnCicle = 2
    execTimeOutPath: str = os.path.join(outDir, "aln_ex_times_ca{:d}_{:s}.tsv".format(alnCicle, os.path.basename(runDir.rstrip("/"))))
    ofd = open(execTimeOutPath, 'w', buffering=1)
    del alnCicle, firstCicle

    # write some message...
    sys.stdout.write('\nPerforming the required {:d} MMseqs2 alignments...'.format(len(requiredAln)))
    # write output when available
    while True:
        try:
            p, s_time, c_time, p_time = results_queue.get(False, 0.01)
            ofd.write('{:s}\t{:.3f}\t{:.3f}\t{:.3f}\t100\t100\t0\n'.format(p, s_time, c_time, p_time))
            #ofd.write('{:s}\t{:s}\t{:s}\t{:s}\n'.format(p, str(s_time), str(c_time), str(p_time)))

        #except queue.Empty:
        except:
            pass
        allExited = True
        for t in runningJobs:
            if t.exitcode is None:
                allExited = False
                break
        if allExited & results_queue.empty():
            break
    ofd.close()

    # this joins the processes after we got the results
    for proc in runningJobs:
        while proc.is_alive():
            proc.join()

    # stop the counter for the alignment time
    sys.stdout.write('\nAll-vs-all alignments elapsed time (seconds):\t{:s}\n'.format(str(round(time.perf_counter() - align_start, 3))))
    #sys.exit("DEBUG :: workers :: perform_mmseqs_multiproc_alignments")
'''



# DEBUG-FUNCTION: this should be removed in future releases
'''
def perform_parallel_essential_alignments(requiredAln: Dict[str, float], protCntDict: Dict[str, int], runDir: str, alnDir: str, create_idx: bool=False, sensitivity: float=4.0, cutoff: int=40, threads: int=4, keepAln: bool=False, debug: bool=False) -> None:
    """Create FASTA subsets in parallel."""
    if debug:
        print("\nperform_parallel_essential_alignments :: START")
        print("Alignments to be performed:\t{:d}".format(len(requiredAln)))
        print("Proteomes:\t{:d}".format(len(protCntDict)))
        print("Directory with run supplementary files: {:s}".format(runDir))
        print("Directory with alignments: {:s}".format(alnDir))
        print("Create MMseqs index files:\t{:s}".format(str(create_idx)))
        print("MMseqs sensitivity:\t{:.2f}".format(sensitivity))
        print("Bitscore cutoff:\t{:d}".format(cutoff))
        print("Threads:\t{:d}".format(threads))
        print("Keep alignment files:\t{:s}".format(str(keepAln)))

    # find the mmseqs2 parser in the source directory
    pySrcDir: str = os.path.dirname(os.path.abspath(__file__))
    mmseqsparser: str = os.path.join(pySrcDir, 'mmseqs_parser_cython.py')
    # copy the file to the output directory
    systools.copy(mmseqsparser, alnDir, metaData=False, debug=False)
    mmseqsparser = os.path.join(alnDir, 'mmseqs_parser_cython.py')
    os.chmod(mmseqsparser, 0o751)
    # find and copy the parser module
    parserModuleFound: bool = False
    for el in os.listdir(pySrcDir):
        if el.startswith('mmseqs_parser_c'):
            if el.endswith('.pyx') or el.endswith('.c'):
                continue
            systools.copy(os.path.join(pySrcDir, el), alnDir, metaData=False, debug=False)
            parserModuleFound = True
            break
    del parserModuleFound, pySrcDir

    # create the queue and start adding
    essential_queue = mp.Queue(maxsize=len(requiredAln) + threads)
    # directory with the original alignments
    originalAlnDir = os.path.join(os.path.dirname(os.path.dirname(runDir)), "alignments")
    if not os.path.isdir(originalAlnDir):
        sys.stderr.write("\nERROR: The directory with alignments was not found.")
        sys.exit(-2)

    # fill the queue with the file paths
    tmpA: str = ""
    tmpB: str = ""
    for pair, weight in requiredAln.items():
        tmpA, tmpB = pair.split("-", 1)
        # proteome pair as tuple: e.g. "1-2" as ("1", "2")
        # and sequence counts for each proteomes
        essential_queue.put(((tmpA, tmpB), protCntDict[tmpA], protCntDict[tmpB]))

    # add flags for ended jobs
    for i in range(0, threads):
        sys.stdout.flush()
        essential_queue.put(None)

    # Queue to contain the execution times
    results_queue = mp.Queue(maxsize=len(requiredAln))

    # get the path to python3 executable
    pythonPath = sys.executable
    # call the method inside workers
    runningJobs = [mp.Process(target=consume_essential_alignments, args=(essential_queue, results_queue, runDir, alnDir, keepAln, sensitivity, cutoff, pythonPath)) for i_ in range(threads)]

    # execute the jobs
    for proc in runningJobs:
        proc.start()

    # open the file in which the time information will be stored
    # use the parent directory name of the database directory as suffix
    execTimeOutPath: str = os.path.join(alnDir, "aln_ex_times_ra_{:s}.tsv".format(os.path.basename(runDir.rstrip("/"))))
    ofd = open(execTimeOutPath, 'w', buffering=1)

    # calculate cpu-time for alignments
    align_start = time.perf_counter()

    # write some message...
    sys.stdout.write('\nPerforming {:d} essential MMseqs2 alignments...'.format(len(requiredAln)))

    # write output when available
    while True:
        try:
            p, s_time, c_time, p_time, seq_pct_a, seq_pct_b, reduction_time = results_queue.get(False, 0.01)
            ofd.write('{:s}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.2f}\t{:.2f}\t{:.3f}\n'.format(p, s_time, c_time, p_time, seq_pct_a, seq_pct_b, reduction_time))

        #except queue.Empty:
        except:
            pass
        allExited = True
        for t in runningJobs:
            if t.exitcode is None:
                allExited = False
                break
        if allExited & results_queue.empty():
            break
    ofd.close()

    # this joins the processes after we got the results
    for proc in runningJobs:
        while proc.is_alive():
            proc.join()
    # stop the counter for the alignment time
    sys.stdout.write('\nAll-vs-all alignments elapsed time (seconds):\t{:s}\n'.format(str(round(time.perf_counter() - align_start, 3))))
'''



def perform_parallel_essential_alignments_plus(requiredAln: Dict[str, Tuple[float, int, int]], protCntDict:Dict[str, int], runDir:str, dbDir:str, alnDir:str, create_idx:bool=True, sensitivity:float=4.0, cutoff:int=40, pmtx:str="blosum62", essentialMode:bool=True, threads:int=4, keepAln:bool=False, compress:bool=False, complev:int=5, debug:bool=False) -> None:
    auxDir: str = os.path.join(runDir, "aux")
    """Create FASTA subsets in parallel."""
    if debug:
        print("\nperform_parallel_essential_alignments_plus :: START")
        print(f"Alignments jobs to be performed:\t{len(requiredAln)}")
        print(f"Proteomes:\t{len(protCntDict)}")
        print(f"Directory containing run files: {runDir}")
        print(f"Directory with auxiliary files: {auxDir}")
        print(f"Directory with shared MMseqs2 databases: {dbDir}")
        print(f"Directory with alignments: {alnDir}")
        print(f"Create MMseqs index files:\t{create_idx}")
        print(f"MMseqs sensitivity:\t{sensitivity:.2f}")
        print(f"Bitscore cutoff:\t{cutoff}")
        print(f"MMseqs2 prefilter substitution matrix:\t{pmtx}")
        print(f"Essential mode:\t{essentialMode}")
        print(f"Threads:\t{threads}")
        print(f"Keep alignment files:\t{keepAln}")
        print(f"Compress output:\t{compress}")
        print(f"Compression level:\t{complev}")

    # identify the species for which the DB should be created
    # Consider only the job in COMPLETE mode
    # Given the pair A-B execute the job type has following values:
    # 0 -> A-B
    # 1 -> B-A only (essentials)
    # 2 -> A-B and B-A (essentials)
    # 3 -> B-A only (complete)
    # 4 -> A-B and B-A (complete)
    reqSpDict: Dict[str, Any] = {}
    for pair, tpl in requiredAln.items():
        jobType = tpl[1]
        if (jobType == 0) or (jobType == 2) or (jobType == 3) or (jobType == 4):
            sp1, sp2 = pair.split('-', 1)
            if not sp1 in reqSpDict:
                reqSpDict[sp1] = None
            if not sp2 in reqSpDict:
                reqSpDict[sp2] = None
            # exit if all the possible species have been inserted
            if len(reqSpDict) == len(protCntDict):
                break

    if len(reqSpDict) > 0:
        fastaDir: str = os.path.join(auxDir, "mapped_input")
        # create the directory which will contain the databases
        systools.makedir(dbDir)
        # Make sure there is enough storage to crate the index files
        # overwrites the create_idx variable
        if create_idx:
            create_idx = check_storage_for_mmseqs_dbs(dbDir, reqSp=len(reqSpDict), gbPerSpecies=0.95, debug=debug)

        # create databases
        sys.stdout.write(f"\nCreating {len(reqSpDict)} MMseqs2 databases...\n")
        # timer for databases creation
        start_time: float = time.perf_counter()

        # create databases in parallel
        perform_parallel_dbs_creation(list(reqSpDict.keys()), fastaDir, dbDir, create_idx=create_idx, threads=threads, debug=debug)
        # end time for databases creation
        end_time: float = time.perf_counter()
        sys.stdout.write(f"\nMMseqs2 databases creation elapsed time (seconds):\t{round(end_time - start_time, 3)}\n")
        # delete timers
        del start_time, end_time

    ''' ########## REMOVE LATER #############
    # Skip the search for the parser file as the parser has been embedded as a function
    # find the mmseqs2 parser in the source directory
    pySrcDir: str = os.path.dirname(os.path.abspath(__file__))
    mmseqsparser: str = os.path.join(pySrcDir, 'mmseqs_parser_cython.py')
    # copy the file to the output directory
    systools.copy(mmseqsparser, alnDir, metaData=False, debug=False)
    mmseqsparser = os.path.join(alnDir, 'mmseqs_parser_cython.py')
    os.chmod(mmseqsparser, 0o751)
    # find and copy the parser module
    parserModuleFound: bool = False
    if debug:
        print("Searching parser file...")
    for el in os.listdir(pySrcDir):
        if el.startswith('mmseqs_parser_c.'):
            if el.endswith('.pyx') or el.endswith('.c'):
                continue
            if debug:
                print("Found parser module:", el)
            systools.copy(os.path.join(pySrcDir, el), alnDir, metaData=False, debug=False)
            parserModuleFound = True
            break
    del parserModuleFound, pySrcDir, mmseqsparser
    ##### REMOVE IF EVERYTHING IS WORKING FINE #####
    ''' 

    # create the queue and start adding
    essential_queue = mp.Queue(maxsize=len(requiredAln) + threads)
    # directory with the original alignments
    originalAlnDir = os.path.join(os.path.dirname(os.path.dirname(runDir)), "alignments")
    if not os.path.isdir(originalAlnDir):
        sys.stderr.write("\nERROR: The directory with alignments was not found.")
        sys.exit(-2)
    # fill the queue with the file paths
    tmpA: str = ""
    tmpB: str = ""
    for pair, tpl in requiredAln.items():
        # tpl contains the following information
        # tpl[0]: float => job weight
        # tpl[1]: int => type of job (e.g, 0-> 1-2 only, 1-> 1-2 and 2-1, etc.)
        # tpl[2]: int => number of threads to be used for the alignment
        tmpA, tmpB = pair.split("-", 1)
        # proteome pair as tuple: e.g. "1-2" as ("1", "2")
        # and sequence counts for each proteomes
        essential_queue.put(((tmpA, tmpB), tpl[1], tpl[2], protCntDict[tmpA], protCntDict[tmpB]))

    # add flags for ended jobs
    for i in range(0, threads):
        sys.stdout.flush()
        essential_queue.put(None)

    # Queue to contain the execution times
    results_queue = mp.Queue(maxsize=len(requiredAln))
    # get the path to python3 executable
    # pythonPath = sys.executable
    # perform the alignments
    
    ### TO REMOVE ###
    # runningJobs = [mp.Process(target=consume_alignment_jobs, args=(essential_queue, results_queue, runDir, dbDir, alnDir, keepAln, sensitivity, cutoff, pmtx, pythonPath)) for i_ in range(threads)]
    #################

    runningJobs = [mp.Process(target=consume_alignment_jobs, args=(essential_queue, results_queue, runDir, dbDir, alnDir, keepAln, sensitivity, cutoff, pmtx, compress, complev)) for i_ in range(threads)]

    # execute the jobs
    for proc in runningJobs:
        proc.start()

    # open the file in which the time information will be stored
    # use the parent directory name of the database directory as suffix
    alnExTimeFileName: str = "aln_ex_times_ra_{:s}.tsv".format(os.path.basename(runDir.rstrip("/")))
    if not essentialMode:
        alnExTimeFileName = "aln_ex_times_ca_{:s}.tsv".format(os.path.basename(runDir.rstrip("/")))
    execTimeOutPath: str = os.path.join(alnDir,alnExTimeFileName )
    del alnExTimeFileName
    ofd = open(execTimeOutPath, "w", buffering=1)

    # calculate cpu-time for alignments
    align_start = time.perf_counter()
    # write some message...
    if debug:
        sys.stdout.write(f"\nPerforming {len(requiredAln)} alignment jobs...")
    # will contain the results from an alignment job
    resList: List[Tuple[str, float, float, float, float, float]] = []

    # write output when available
    while True:
        try:
            resList = results_queue.get(False, 0.01)
            for resTpl in resList:
                ofd.write('{:s}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.2f}\t{:.2f}\t{:.3f}\n'.format(*resTpl))
        #except queue.Empty:
        except:
            pass
        allExited = True
        for t in runningJobs:
            if t.exitcode is None:
                allExited = False
                break
        if allExited & results_queue.empty():
            break
    ofd.close()

    # this joins the processes after we got the results
    for proc in runningJobs:
        while proc.is_alive():
            proc.join()

    # stop the counter for the alignment time
    sys.stdout.write(f"\nAll-vs-all alignments elapsed time (seconds):\t{round(time.perf_counter() - align_start, 3)}\n")
    # sys.exit("DEBUG: @workers.perform_parallel_essential_alignments_plus, after Starting jobs")



# DEBUG-FUNCTION: this should be removed in future releases
'''
def perform_parallel_orthology_inference(requiredPairsDict, inDir, outDir=os.getcwd(), sharedDir=None, cutoff=40, confCutoff=0.05, lenDiffThr=0.5, threads=8, debug=False):
    """Execute orthology inference for the required pairs."""
    if debug:
        print('\nperform_parallel_orthology_inference :: START')
        print('Proteome pairs to be processed:\t{:d}'.format(len(requiredPairsDict)))
        print('Input directory:{:s}'.format(inDir))
        print('Outdir:{:s}'.format(outDir))
        print('Alignment directory:{:s}'.format(sharedDir))
        print('Cutoff:\t{:d}'.format(cutoff))
        print('Confidence cutoff for paralogs:\t{:s}'.format(str(confCutoff)))
        print('Length difference filtering threshold:\t{:s}'.format(str(lenDiffThr)))
        print('CPUs (for mmseqs):\t{:d}'.format(threads))
    # make sure that the directory with alignments exists
    if not os.path.isdir(sharedDir):
        sys.stderr.write("ERROR: The directory with the alignment files\n{:s}\nwas not found, please provide a valid path.\n".format(sharedDir))
        sys.exit(-2)
    if not os.path.isdir(inDir):
        sys.stderr.write("ERROR: The directory with the input files\n{:s}\nwas not found, please provide a valid path.\n".format(inDir))
        sys.exit(-2)
    #create the output directory if does not exist yet
    if outDir != os.getcwd():
        if not os.path.isdir(outDir):
            systools.makedir(outDir)
    if outDir[-1] != '/':
        outDir += '/'
    # check if the output directory differs from the input one
    if os.path.dirname(inDir) == os.path.dirname(outDir):
        sys.stderr.write("\nERROR: the output directory {:s}\nmust be different from the one in which the input files are stored\n{:s}\n".format(outDir, inDir))
        sys.exit(-3)
    # check cutoff
    if cutoff < 30:
        cutoff = 40
    # create the queue and start adding the jobs
    jobs_queue = mp.Queue()

    # fill the queue with the processes
    for pair in requiredPairsDict:
        jobs_queue.put(pair)
    # add flags for eneded jobs
    for i in range(0, threads):
        jobs_queue.put(None)

    # Queue to contain the execution time
    results_queue = mp.Queue(maxsize=len(requiredPairsDict))
    # call the method inside workers
    runningJobs = [mp.Process(target=consume_orthology_inference_jobs, args=(jobs_queue, results_queue, inDir, outDir, sharedDir, cutoff, confCutoff, lenDiffThr, threads, debug)) for i_ in range(threads)]

    for proc in runningJobs:
        proc.start()

    # open the file in which the time information will be stored
    execTimeOutPath = os.path.join(sharedDir, 'orthology_ex_time_{:s}.tsv'.format(os.path.basename(outDir.rstrip('/'))))
    ofd = open(execTimeOutPath, 'w', buffering=1)

    # get the results from the queue without filling the Pipe buffer
    while True:
        try:
            p, val = results_queue.get(False, 0.01)
            ofd.write('{:s}\t{:s}\n'.format(p, str(val)))
        except queue.Empty:
            pass
        allExited = True
        for t in runningJobs:
            if t.exitcode is None:
                allExited = False
                break
        if allExited & results_queue.empty():
            break
    ofd.close()

    for proc in runningJobs:
        while proc.is_alive():
            proc.join()
'''



def perform_parallel_orthology_inference_shared_dict(requiredPairsDict, inDir, outDir=os.getcwd(), sharedDir=None, sharedWithinDict=None, cutoff=40, confCutoff=0.05, lenDiffThr=0.5, threads=8, compressed:bool=False, debug=False):
    """Execute orthology inference for the required pairs."""
    if debug:
        print("\nperform_parallel_orthology_inference_shared_dict :: START")
        print(f"Proteome pairs to be processed:\t{len(requiredPairsDict)}")
        print(f"Input directory: {inDir}")
        print(f"Outdir: {outDir}")
        print(f"Alignment directory: {sharedDir}")
        print(f"Shared within-align dictionaries:\t{len(sharedWithinDict)}")
        print(f"Cutoff:\t{cutoff}")
        print(f"Confidence cutoff for paralogs:\t{confCutoff}")
        print(f"Length difference filtering threshold:\t{lenDiffThr}")
        print(f"CPUs (for mmseqs):\t{threads}")
        print(f"Compressed alignment files:\t{compressed}")
    # make sure that the directory with alignments exists
    if not os.path.isdir(sharedDir):
        sys.stderr.write(f"ERROR: The directory with the alignment files\n{sharedDir}\nwas not found, please provide a valid path\n")
        sys.exit(-2)
    if not os.path.isdir(inDir):
        sys.stderr.write(f"ERROR: The directory with the input files\n{inDir}\nwas not found, please provide a valid path\n")
        sys.exit(-2)
    #create the output directory if does not exist yet
    if outDir != os.getcwd():
        if not os.path.isdir(outDir):
            systools.makedir(outDir)
    # check if the output directory differs from the input one
    if os.path.dirname(inDir) == os.path.dirname(outDir):
        sys.stderr.write(f"\nERROR: the output directory {outDir}\nmust be different from the one in which the input files are stored\n{inDir}\n")
        sys.exit(-2)
    # check cutoff
    if cutoff < 30:
        cutoff = 40
    # create the queue and start adding the jobs
    jobs_queue = mp.Queue()

    # fill the queue with the processes
    for pair in requiredPairsDict:
        jobs_queue.put(pair)
    # add flags for eneded jobs
    for i in range(0, threads):
        jobs_queue.put(None)

    # Queue to contain the execution time
    results_queue = mp.Queue(maxsize=len(requiredPairsDict))
    # call the method inside workers
    runningJobs = [mp.Process(target=consume_orthology_inference_sharedict, args=(jobs_queue, results_queue, inDir, outDir, sharedDir, sharedWithinDict, cutoff, confCutoff, lenDiffThr, threads, compressed)) for i_ in range(threads)]

    for proc in runningJobs:
        proc.start()

    # open the file in which the time information will be stored
    execTimeOutPath = os.path.join(sharedDir, "orthology_ex_time_{:s}.tsv".format(os.path.basename(outDir.rstrip("/"))))
    ofd = open(execTimeOutPath, "w", buffering=1)

    # update the shared dictionary
    # and remove the shared dictionary if required
    # get the results from the queue without filling the Pipe buffer
    gcCallSentinel: int = 2 * threads
    whileCnt: int = 0
    wtCnt: int = 0
    gcCallCnt: int = 0
    while True:
        try:
            p, val = results_queue.get(False, 0.01)
            ofd.write("{:s}\t{:s}\n".format(p, str(val)))
            whileCnt += 1
            wtCnt += 1
            #'''
            sp1, sp2 = p.split("-", 1)
            # decrease the counters in the shared dictionaries
            sharedWithinDict[sp1][0] -= 1
            if sharedWithinDict[sp1][0] == 0:
                del sharedWithinDict[sp1]
                # call the garbage collector to free memory explicitly
                gc.collect()
                if debug:
                    print(f"Removed dictionary for {sp1}")
                    print(f"Remaining shared dictionaries:\t{len(sharedWithinDict)}")
            sharedWithinDict[sp2][0] -= 1
            if sharedWithinDict[sp2][0] == 0:
                del sharedWithinDict[sp2]
                gc.collect()
                if debug:
                    print(f"Removed dictionary for {sp2}")
                    print(f"Remaining shared dictionaries:\t{len(sharedWithinDict)}")
            # call the garbage collector if a given number ortholog tables
            # has been generated
            if whileCnt == gcCallSentinel:
                gc.collect()
                whileCnt = 0
                gcCallCnt += 1
                if debug:
                    print(f"\ngc.collect() call:\t{gcCallCnt}\nCompleted tables:\t{wtCnt}")

        except queue.Empty:
            pass
        allExited = True
        for t in runningJobs:
            if t.exitcode is None:
                allExited = False
                break
        if allExited & results_queue.empty():
            break
    ofd.close()

    for proc in runningJobs:
        while proc.is_alive():
            proc.join()