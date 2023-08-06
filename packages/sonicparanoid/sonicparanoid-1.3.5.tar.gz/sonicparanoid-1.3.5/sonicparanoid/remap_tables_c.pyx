from libc.stdio cimport *
# from libc.stdlib cimport atoi
# from libc.stdlib cimport atof
import sys
import os
import pickle
import multiprocessing as mp
from typing import Dict, List

cdef extern from "stdio.h":
    #FILE * fopen ( const char * filename, const char * mode )
    FILE *fopen(const char *, const char *)
    #int fclose ( FILE * stream )
    int fclose(FILE *)
    #ssize_t getline(char **lineptr, size_t *n, FILE *stream);
    ssize_t getline(char **, size_t *, FILE *)



### Worker functions (1 cpu) ###
def consume_remap_pairwise_relations(jobs_queue, results_queue, inTblRoot:str, outTblRoot:str,  new2OldHdrAllSp: Dict[str, Dict[str, str]]) -> None:
    """Remap pairsire relation using 1 cpu."""
    # jobs_queue contains tuples with input and output paths
    while True:
        current_input = jobs_queue.get(True, 1)
        if current_input is None:
            break
        A, B = current_input[0]
        inTbl: str = os.path.join(inTblRoot, f"{A}/{A}-{B}/table.{A}-{B}")
        remappedA, remappedB = current_input[1]
        outTbl: str = os.path.join(outTblRoot, f"{remappedA}/{remappedA}-{remappedB}")
        makedir(os.path.dirname(outTbl))
        # remap pairwise relations
        if A == B:
          remap_pairwise_relations(inTbl, outTbl, new2OldHdrAllSp[A], new2OldHdrAllSp[A], debug=False)
        else:
          remap_pairwise_relations(inTbl, outTbl, new2OldHdrAllSp[A], new2OldHdrAllSp[B], debug=False)
        # add the computed pair
        results_queue.put((f"{A}-{B}", f"{remappedA}-{remappedB}"))
        # sys.exit("DEBUG@remap_tables_c.pyx -> consume_remap_pairwise_relations")



### Job processing Functions
def remap_pairwise_relations_parallel(pairsFile, runDir=os.getcwd(), orthoDbDir=os.getcwd(), threads=4, debug=False) -> None:
    """Remap pairwise ortholog relations in parallel."""
    auxDir: str = os.path.join(runDir, "aux")
    inputSeqInfoDir: str = os.path.join(auxDir, "input_seq_info")
    if debug:
        print("\nremap_pairwise_relations_parallel :: START")
        print(f"File with pairs to be mapped: {pairsFile}")
        print(f"Run directory: {runDir}")
        print(f"Directory with auxiliary files: {auxDir}")
        print(f"Directory with ortholog relations to be mapped: {orthoDbDir}")
        print(f"Threads:\t{threads}")
    # get input files paths
    # inPaths: List[str] = []
    A: str = ""
    B: str = ""
    tblCnt: int = 0
    spCnt: int = 0
    tmpTpl: Tuple[str, str] = ("", "") 
    # load all mapping dictionaries
    new2OldHdrAllSp: Dict[str, Dict[str, str]] = {}
    id2SpDict: Dict[str, str] = {}
    # File with species mapping info
    speciesFile = os.path.join(auxDir, "species.tsv")
    # output directory for remapped tables
    remapOutDir = os.path.join(runDir, "pairwise_orthologs/")

    # load the species IDs mapping
    for ln in open(speciesFile, "r"):
      mapId, spName, d1 = ln.split("\t", 2)
      spCnt += 1
      if not mapId in id2SpDict:
        id2SpDict[mapId] = spName

    # create the queue and start adding
    combinations: int = int(spCnt * ((spCnt - 1) / 2))
    remap_queue = mp.Queue(maxsize=combinations + threads)

    # fill the queue with tples containing the original and remapped species names
    # EXAMPLE: (A, B) and mapped species names (remap(A), remap(B))
    # and load the pickle files
    for pair in open(pairsFile, "r"):
      A, B = pair[:-1].split("-", 1)
      tblCnt += 1
      sys.stdout.flush()
      # load the mapping dictionaries if necessary
      if A not in new2OldHdrAllSp:
        # load the pickle
        tmpPickle = os.path.join(inputSeqInfoDir, f"hdr_{A}.pckl")
        with open(tmpPickle, "br") as fd:
          new2OldHdrAllSp[A] = pickle.load(fd)
      # now do the same thing for B
      if B not in new2OldHdrAllSp:
        # load the pickle
        tmpPickle = os.path.join(inputSeqInfoDir, f"hdr_{B}.pckl")
        with open(tmpPickle, "br") as fd:
          new2OldHdrAllSp[B] = pickle.load(fd)
      # Add Tuples with Tuples of input Species IDs (A, B) and mapped species names (remap(A), remap(B))
      remap_queue.put(((A, B), (id2SpDict[A], id2SpDict[B])))
    if debug:
      print(f"Input species:\t{spCnt}")
      print(f"Pairwise tables to be remapped:\t{combinations}")

    # add flags for completed jobs
    for i in range(0, threads):
        sys.stdout.flush()
        remap_queue.put(None)
    # Queue to contain the execution time
    results_queue = mp.Queue(maxsize=combinations)

    # call the method inside workers
    runningJobs = [mp.Process(target=consume_remap_pairwise_relations, args=(remap_queue, results_queue, orthoDbDir, remapOutDir, new2OldHdrAllSp)) for i_ in range(threads)]

    for proc in runningJobs:
        proc.start()

    while True:
        try:
            rawPair, remapPair = results_queue.get(False, 0.01)
            #debug = True
            if debug:
              sys.stdout.write(f"Remapping done for:\t{rawPair} -> {remapPair}\n")
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

    # this joins the processes after we got the results
    for proc in runningJobs:
        while proc.is_alive():
            proc.join()
    # sys.exit("DEBUG@remap_tables_c.pyx -> remap_pairwise_relations_parallel")



#### Other functions ####

def remap_pairwise_relations(inTbl: str, outTbl: str, old2NewHdrDictA: Dict[str, str], old2NewHdrDictB: Dict[str, str], debug=False) -> None:
    """Read a table with pairwise relations and add the original FASTA header."""
    if debug:
        print(f"\nremap_pairwise_relations (Cython) :: START")
        print(f"Input table: {inTbl}")
        print(f"Output table: {outTbl}")
        print(f"Headers to remap for species A:\t{len(old2NewHdrDictA)}")
        print(f"Headers to remap for species B:\t{len(old2NewHdrDictB)}")
    if not os.path.isfile(inTbl):
        sys.stderr.write(f"\nThe file {inTbl} was not found,\nplease provide a valid input path.\n")
        sys.exit(-2)

    # sample table line
    #OrtoId	Score	OrtoA	OrtoB
    #14\t620\t1.49 1.0\t3.1653 1.0 3.373 0.385

    # define the variables
    clstrId: str = ""
    clstrSc: str = ""
    clstrLx: str = "" # part from species A
    clstrRx: str = "" # part from species B
    newClstr: str = "" # remapped string
    # list to be used during the split
    tmpListLx: List[str] = []
    tmpListRx: List[str] = []

    # other variables
    cdef int rdCnt
    rdCnt = 0
    cdef int wrtCnt
    wrtCnt = 0
    # define file names and file descriptor pointer in C
    filename_byte_string = inTbl.encode("UTF-8")
    cdef char* inTbl_c = filename_byte_string
    #file pointer
    cdef FILE* cfile
    # varibales for files and lines
    cdef char * line = NULL
    cdef size_t l = 0
    cdef ssize_t read
    clstrId: str = ""
    clstrSc: str = ""
    clstrLx: str = ""
    clstrRx: str = ""
    tmpStrRx: str = ""
    tmpStrLx: str = ""
    tmpListLx: List[str] = []
    tmpListRx: List[str] = []

    #open the pairwise ortholog table
    cfile = fopen(inTbl_c, "rb")
    if cfile == NULL:
        raise FileNotFoundError(2, f"No such file or directory: '{inTbl_c}'" )

    # open the output file
    ofd = open(outTbl, "w")
    # read the file, remap the ids and write in the new output table
    while True:
        read = getline(&line, &l, cfile)
        if read == -1:
            break
        rdCnt += 1

        # if the last letter is a 'B' then it is the cluster headers
        if line.decode()[-2] == "B":
          ofd.write(line.decode())
          wrtCnt += 1
          continue
        # split the cluster string
        flds = line.split(b'\t', 3)
        clstrId = flds[0].decode()
        clstrSc = flds[1].decode()
        clstrLx = flds[2].decode()
        clstrRx = flds[3].decode()

        # map elements of the left part of the cluster
        # example: 3.1653 1.0 3.373 0.385 -> gene1 1.0 gene2 0.385
        tmpListLx = clstrLx.split(" ")
        for i, val in enumerate(tmpListLx):
          if i % 2 == 0: # then we map the FASTA header
            tmpListLx[i] = old2NewHdrDictA[val]

        # map elements of the right part of the cluster
        tmpListRx = clstrRx.split(" ")
        for i, val in enumerate(tmpListRx):
          if i % 2 == 0: # then we map the FASTA header
            tmpListRx[i] = old2NewHdrDictB[val]

        # ofd.write("{:s}\t{:s}\t{:s}\t{:s}".format(clstrId, clstrSc, " ".join(tmpListLx), " ".join(tmpListRx)))
        tmpStrLx = " ".join(tmpListLx)
        tmpStrRx = " ".join(tmpListRx)
        ofd.write(f"{clstrId}\t{clstrSc}\t{tmpStrLx}\t{tmpStrRx}")
        wrtCnt += 1

    #close input file
    fclose(cfile)
    # sys.exit("DEBUG@remap_tables_c.pyx -> remap_pairwise_relations")


def makedir(path):
    """Create a directory including the intermediate directories in the path if not existing."""
    # check the file or dir does not already exist
    if os.path.isfile(path):
        sys.stderr.write(f"\nWARNING: {path}\nalready exists as a file, and the directory cannot be created.\n")
    try:
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise
