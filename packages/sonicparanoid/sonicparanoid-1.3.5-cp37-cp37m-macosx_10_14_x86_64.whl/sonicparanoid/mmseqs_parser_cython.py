import os
import sys
from mmseqs_parser_c import mmseqs_parser_7flds
from subprocess import run

########### FUNCTIONS ############
def get_params():
    """Parse and analyse command line parameters."""
    import argparse
    parser_usage = "\nProvide an input file generated using mmseqs2 and converted into BLASTP compatible tab-separated format.\nOutputs a file of ortholog and paralogs that can be processed by InParanoid.\n"
    parser = argparse.ArgumentParser(description="mmseqs2 parser 1.3.4", usage=parser_usage)
    #start adding the command line options
    parser.add_argument("-i", "--input", type=str, required=True, help="Tab-separated alignment file generated using mmseqs2 and converted in BLASTP tab-separated format.\nNOTE: for details on the fields contained in the output refer to function inparanoid_like_parser", default=None)
    parser.add_argument("-q", "--query", type=str, required=True, help="FASTA file with the query proteins.", default=None)
    parser.add_argument("-t", "--db", type=str, required=True, help="FASTA file with the target proteins.", default=None)
    parser.add_argument("-o", "--output", type=str, required=True, help="File in which the output will be stored.", default=None)
    parser.add_argument("-r", "--run-dir", type=str, required=False, help="Directory in which the files with sequence lengths are stored.", default=None)
    parser.add_argument("-c", "--cutoff", type=int, required=False, help="Cutoff score (sum of hsp bitscores for each hit) for alignments.", default=40)
    parser.add_argument("-co", "--compress", required=False, help="Archive the generated parser file.", default=False, action="store_true")
    parser.add_argument("-cl", "--compression-lev", type=int, required=False, help="Gzip compression level.", default=5)
    parser.add_argument("-d", "--debug", required=False, help="Output debug information.\nNOTE: this is not used when the input is STDIN.", default=False, action="store_true")
    args = parser.parse_args()
    return (args, parser)



########### MAIN ############
def main():
    #Get the parameters
    args = get_params()[0]
    debug: bool = args.debug
    compress: bool = args.compress
    complev: int = args.compression_lev
    inputPath = os.path.realpath(args.input)
    queryPath = targetPath = ""
    if args.query:
        queryPath = os.path.realpath(args.query)
    if args.db:
        targetPath = os.path.realpath(args.db)
    outPath = os.path.realpath(args.output)
    cutoff = args.cutoff
    outName = os.path.basename(outPath)
    outDir = os.path.dirname(outPath)
    # directory containing input mapping files, pickles
    # infer from the input file (queryPath)
    runDir: str = ""
    if args.run_dir is not None:
        runDir = os.path.realpath(args.run_dir)
    else:
        runDir = queryPath.rsplit("/", 2)[0]

    if debug:
        print(f"Alignment file:\t{inputPath}")
        print(f"Query file:\t{queryPath}")
        print(f"Target file:\t{targetPath}")
        print(f"Output file:\t{outPath}")
        print(f"Run dir:\t{runDir}")
        print(f"Cutoff:\t{cutoff}")
        print(f"Compress:\t{compress}")
        if compress:
            print(f"Compression level:\t{complev}")

    # use pickle files
    qSeqLenPath = os.path.join(runDir, f"{os.path.basename(queryPath)}.len.pckl")
    tSeqLenPath = os.path.join(runDir, f"{os.path.basename(targetPath)}.len.pckl")

    ########## sort the BLAST output ###########
    # sort blast_output -k1,1 -k2,2 -k12nr > sorted_output
    bsName: str = os.path.basename(inputPath)
    sortPath: str = os.path.join(outDir, f"sorted_{bsName}")

    # sort(inputPath, '-k1,1', '-k2,2', '-k7nr', _out=ofd)

    sortCmd: str = f"sort -o {sortPath} -k1,1 -k2,2 -k7nr {inputPath}"
    # use run
    run(sortCmd, shell=True)

    if not os.path.isfile(inputPath):
        sys.stderr.write(f"WARNING: the file\n{inputPath}\nwas not found...")
    # remove the unsorted output and rename
    os.remove(inputPath)
    os.rename(sortPath, inputPath)
    ############################################
    
    # Parse the MMseqs2 output
    mmseqs_parser_7flds(inputPath, qSeqLenPath, tSeqLenPath, outDir=outDir, outName=outName, scoreCoff=cutoff, compress=compress, complev=complev, debug=debug)


if __name__ == "__main__":
    main()
