from libc.stdio cimport *
from libc.stdlib cimport atoi
from libc.stdlib cimport atof
import sys
import os
import pandas as pd
from collections import OrderedDict
from typing import Dict, List, Tuple



cdef extern from "stdio.h":
    #FILE * fopen ( const char * filename, const char * mode )
    FILE *fopen(const char *, const char *)
    #int fclose ( FILE * stream )
    int fclose(FILE *)
    #ssize_t getline(char **lineptr, size_t *n, FILE *stream);
    ssize_t getline(char **, size_t *, FILE *)



def equalize_AB_and_BA_scores_fast(abScores, baScores, debug=False):
    """Equalize the scores from AB and BA alignments."""
    # for example given the hit g-c in AB with score x,
    # and given the hits c-g in BA with score y
    # a uniq values for BA[c-g] and AB[g-c] are calculated and the corresponding
    # dictionaries updated accordingly
    if debug:
        print("equalize_AB_and_BA_scores_fast :: START")
        print(f"Hits for AB: {len(abScores)}")
        print(f"Hits for BA: {len(baScores)}")
    # check input lengths
    if len(abScores) != len(baScores):
        sys.write.stderr("ERROR: the two dictionaries must contain the same number of hits.")
        sys.exit(-5)

    # temporary variables
    cdef float scAB, scBA
    cdef int avgScore
    q: str = ""
    s: str = ""
    k: str = ""
    k2: str = ""

    #start looping the hits in AB
    for k in abScores:
        scAB = abScores[k]
        #get revese key
        q, s = k.split("!", 1)
        k2 = f"{s}!{q}"
        scBA = baScores[k2]
        #calculate the average value
        #correct rounding
        avgScore = <int>round(float((scAB + scBA) / 2.), 0)
        #print(avgScore)
        abScores[k] = baScores[k2] = avgScore
    return (abScores, baScores)



def load_between_proteomes_scores_fast(alignFileAB, alignFileBA, covCoff=0.25, overlapCoff=0.5, scoreCoff=40, debug=False):
    """Load between proteomes scores for AB and BA alignments (Cython)."""
    if debug:
      print("load_between_proteomes_scores_fast :: START")
      print(f"Input AB: {alignFileAB}")
      print(f"Input BA: {alignFileBA}")
      print(f"Coverage cutoff:\t{covCoff}")
      print(f"Overlap cutoff:\t{overlapCoff}")
      print(f"Overlap cutoff:\t{scoreCoff}")
    if not os.path.isfile(alignFileAB):
        sys.stderr.write(f"The file {alignFileAB} was not found, please provide a valid input path")
        sys.exit(-2)
    if not os.path.isfile(alignFileBA):
        sys.stderr.write(f"The file {alignFileBA} was not found, please provide a valid input path")
        sys.exit(-2)
    #create the dictionaries to store the ids and scores
    scoreAB = OrderedDict()
    scoreBA = OrderedDict()
    hitsAinB = OrderedDict()
    hitsBinA = OrderedDict()
    # will contain the sequence lengths
    betweenLenDictA = OrderedDict() # only A related genes
    betweenLenDictB = OrderedDict() # only B related genes

    # define file names and file descriptor pointer in C
    filename_byte_string = alignFileAB.encode("UTF-8")
    cdef char* alignFileABc = filename_byte_string
    # convert the second input file name to bytestring
    filename_byte_string = alignFileBA.encode("UTF-8")
    cdef char* alignFileBAc = filename_byte_string
    #file pointer
    cdef FILE* cfile
    # varibales for files and lines
    cdef char * line = NULL
    cdef size_t l = 0
    cdef ssize_t read

    # define the variables that will be used
    cdef int qlen, slen, qAggrMatch, sAggrMatch, qLocMatch, sLocMatch, lnCntAB, overlapSkipCntAB, lowScoreCntAB, okCntAB
    cdef float score, overlapCoff_c, scoreCoff_c, covCoff_c
    covCoff_c = <float>covCoff
    scoreCoff_c = <float>scoreCoff
    overlapCoff_c = <float>overlapCoff
    #initialize counters
    lnCntAB: int = 0
    overlapSkipCntAB: int = 0
    lowScoreCntAB: int = 0
    okCntAB: int = 0
    q: str = ""
    s: str = ""

    #open the alignments for AB
    cfile = fopen(alignFileABc, "rb")
    # read the file and load hits for AA
    while True:
        read = getline(&line, &l, cfile)
        if read == -1:
            break

        #split the string
        flds = line.split(b'\t', 8)
        # convert bytes to strings
        q = flds[0].decode()
        s = flds[1].decode()
        score = atof(flds[2])
        qlen = atoi(flds[3])
        slen = atoi(flds[4])
        qAggrMatch = atoi(flds[5])
        sAggrMatch = atoi(flds[6])
        qLocMatch = atoi(flds[7])
        sLocMatch = atoi(flds[8])
        #check if the alignment should be used
        ''' This should never happen!
        if score < scoreCoff_c:
            lowScoreCntAB += 1
            continue
        '''
        if overlap_test_c(qlen, slen, qAggrMatch, sAggrMatch, qLocMatch, sLocMatch, covCoff_c, overlapCoff_c) == 1:
            overlapSkipCntAB += 1
            #if s == 'G0MEW7':
              #print(line)
              #sys.exit('DEBUG :: load_between_proteomes_scores_fast')
            continue
        okCntAB += 1
        #now same the hit scores
        hitId = '%s!%s'%(q, s)
        hitIdRev = '%s!%s'%(s, q)
        # add sequence lengths in dictionary
        if not q in betweenLenDictA:
          betweenLenDictA[q] = qlen
        if not s in betweenLenDictB:
          betweenLenDictB[s] = slen
        #save the score
        scoreAB[hitId] = score
        #add match and scores for each query sequence
        if not q in hitsAinB:
            hitsAinB[q] = OrderedDict()
        hitsAinB[q][s] = score
        #initialize the mutual score to the score cut-off
        scoreBA[hitIdRev] = scoreCoff
    #close input file
    fclose(cfile)

    # define the variables that will be used for BB
    cdef int overlapSkipCntBB, lowScoreCntBB, okCntBB
    #initialize counters
    overlapSkipCntBA: int = 0
    lowScoreCntBA: int = 0
    okCntBA: int = 0

    #open the alignments for AB
    cfile = fopen(alignFileBAc, "rb")
    # read the file and load hits for AA
    while True:
        read = getline(&line, &l, cfile)
        if read == -1:
            break

        #split the string
        flds = line.split(b'\t', 8)
        # convert bytes to strings
        q = flds[0].decode()
        s = flds[1].decode()
        score = atof(flds[2])
        qlen = atoi(flds[3])
        slen = atoi(flds[4])
        qAggrMatch = atoi(flds[5])
        sAggrMatch = atoi(flds[6])
        qLocMatch = atoi(flds[7])
        sLocMatch = atoi(flds[8])

        #check if the alignment should be used
        ''' This should never happen!
        if score < scoreCoff_c:
            lowScoreCntBA += 1
            continue
        '''
        if overlap_test_c(qlen, slen, qAggrMatch, sAggrMatch, qLocMatch, sLocMatch, covCoff_c, overlapCoff_c) == 1:
            overlapSkipCntBA += 1
            continue
        okCntBA += 1
        #now same the hit scores
        hitId = '%s!%s'%(q, s)
        hitIdRev = '%s!%s'%(s, q)
        # add sequence lengths in dictionaries
        if not q in betweenLenDictB:
          betweenLenDictB[q] = qlen
        if not s in betweenLenDictA:
          betweenLenDictA[s] = slen
        #save the score
        scoreBA[hitId] = score
        #if hitRev is not present in AB
        if not hitIdRev in scoreAB:
            scoreAB[hitIdRev] = scoreCoff
        #add match and scores for each query sequence
        if not q in hitsBinA:
            hitsBinA[q] = OrderedDict()
        hitsBinA[q][s] = score
    #close input file
    fclose(cfile)

    # sort the AB hits by best score
    for query in hitsAinB:
        tmpDict = hitsAinB[query]
        if len(tmpDict) == 1:
            continue
        #update with the sorted ditionary
        tplList = [(k, tmpDict[k]) for k in sorted(tmpDict, key=tmpDict.get, reverse=True)]
        tmpDict = OrderedDict()
        for tpl in tplList:
            tmpDict[tpl[0]] = tpl[1]
        hitsAinB[query] = tmpDict
    # sort the BA hits by best score
    for query in hitsBinA:
        tmpDict = hitsBinA[query]
        if len(tmpDict) == 1:
            continue
        #update with the sorted ditionary
        tplList = [(k, tmpDict[k]) for k in sorted(tmpDict, key=tmpDict.get, reverse=True)]
        tmpDict = OrderedDict()
        for tpl in tplList:
            tmpDict[tpl[0]] = tpl[1]
        hitsBinA[query] = tmpDict
    if debug:
        print(f"Loaded sequence lengths for A:\t{len(betweenLenDictA)}")
        print(f"Loaded sequence lengths for B:\t{len(betweenLenDictB)}")
        print(f"\nLoaded hits AB:\t{len(scoreAB)}")
        print(f"Query sequences in A with orthologs in B:\t{len(hitsAinB)}")
        print(f"Overlap fail AB:\t{overlapSkipCntAB}")
        print(f"Low score AB:\t{lowScoreCntAB}")
        print(f"OK alignments AB:\t{okCntAB}")
        print(f"\nLoaded hits BA:\t{len(scoreBA)}")
        print(f"Query sequences in B with orthologs in A:\t{len(hitsBinA)}")
        print(f"Overlap fail BA:\t{overlapSkipCntBA}")
        print(f"Low score BA:\t{lowScoreCntBA}")
        print(f"OK alignments BA:\t{okCntBA}")
    #return the dictionaries
    return (scoreAB, hitsAinB, scoreBA, hitsBinA, betweenLenDictA, betweenLenDictB)



def load_between_proteomes_scores_compressed(alignFileAB, alignFileBA, covCoff=0.25, overlapCoff=0.5, scoreCoff=40, debug=False):
    """Load between proteomes scores for AB and BA alignments from compressed alignment file."""
    import gzip
    if debug:
      print("load_between_proteomes_scores_compressed :: START")
      print(f"Input AB: {alignFileAB}")
      print(f"Input BA: {alignFileBA}")
      print(f"Coverage cutoff:\t{covCoff}")
      print(f"Overlap cutoff:\t{overlapCoff}")
      print(f"Overlap cutoff:\t{scoreCoff}")
    if not os.path.isfile(alignFileAB):
        sys.stderr.write(f"The file {alignFileAB} was not found, please provide a valid input path")
        sys.exit(-2)
    if not os.path.isfile(alignFileBA):
        sys.stderr.write(f"The file {alignFileBA} was not found, please provide a valid input path")
        sys.exit(-2)
    #create the dictionaries to store the ids and scores
    scoreAB = OrderedDict()
    scoreBA = OrderedDict()
    hitsAinB = OrderedDict()
    hitsBinA = OrderedDict()
    # will contain the sequence lengths
    betweenLenDictA = OrderedDict() # only A related genes
    betweenLenDictB = OrderedDict() # only B related genes

    # define the variables that will be used
    cdef int qlen, slen, qAggrMatch, sAggrMatch, qLocMatch, sLocMatch, lnCntAB, overlapSkipCntAB, lowScoreCntAB, okCntAB
    cdef float score, overlapCoff_c, scoreCoff_c, covCoff_c
    covCoff_c = <float>covCoff
    scoreCoff_c = <float>scoreCoff
    overlapCoff_c = <float>overlapCoff
    #initialize counters
    lnCntAB: int = 0
    overlapSkipCntAB: int = 0
    lowScoreCntAB: int = 0
    okCntAB: int = 0
    q: str = ""
    s: str = ""
    line: bytes = bytes()
    flds: List[bytes] = []

    #open the alignments for AB
    with gzip.open(alignFileAB, "rb") as gzifd:
        # read the file and extract hits of A in B
        for line in gzifd.readlines():
            #split the string
            flds = line.split(b"\t", 8)
            # convert bytes to strings
            q = flds[0].decode()
            s = flds[1].decode()
            score = atof(flds[2])
            qlen = atoi(flds[3])
            slen = atoi(flds[4])
            qAggrMatch = atoi(flds[5])
            sAggrMatch = atoi(flds[6])
            qLocMatch = atoi(flds[7])
            sLocMatch = atoi(flds[8])
            #check if the alignment should be used
            ''' This should never happen!
            if score < scoreCoff_c:
                lowScoreCntAB += 1
                continue
            '''
            if overlap_test_c(qlen, slen, qAggrMatch, sAggrMatch, qLocMatch, sLocMatch, covCoff_c, overlapCoff_c) == 1:
                overlapSkipCntAB += 1
                continue
            okCntAB += 1
            #now same the hit scores
            hitId = '%s!%s'%(q, s)
            hitIdRev = '%s!%s'%(s, q)
            # add sequence lengths in dictionary
            if not q in betweenLenDictA:
                betweenLenDictA[q] = qlen
            if not s in betweenLenDictB:
                betweenLenDictB[s] = slen
            #save the score
            scoreAB[hitId] = score
            #add match and scores for each query sequence
            if not q in hitsAinB:
                hitsAinB[q] = OrderedDict()
            hitsAinB[q][s] = score
            #initialize the mutual score to the score cut-off
            scoreBA[hitIdRev] = scoreCoff

    # define the variables that will be used for BB
    cdef int overlapSkipCntBB, lowScoreCntBB, okCntBB
    #initialize counters
    overlapSkipCntBA: int = 0
    lowScoreCntBA: int = 0
    okCntBA: int = 0
    flds.clear()
    line = bytes()

    #open the alignments for BA
    with gzip.open(alignFileBA, "rb") as gzifd:
        # read the file and extract hits of B in A
        for line in gzifd.readlines():

            #split the string
            flds = line.split(b'\t', 8)
            # convert bytes to strings
            q = flds[0].decode()
            s = flds[1].decode()
            score = atof(flds[2])
            qlen = atoi(flds[3])
            slen = atoi(flds[4])
            qAggrMatch = atoi(flds[5])
            sAggrMatch = atoi(flds[6])
            qLocMatch = atoi(flds[7])
            sLocMatch = atoi(flds[8])

            #check if the alignment should be used
            ''' This should never happen!
            if score < scoreCoff_c:
                lowScoreCntBA += 1
                continue
            '''
            if overlap_test_c(qlen, slen, qAggrMatch, sAggrMatch, qLocMatch, sLocMatch, covCoff_c, overlapCoff_c) == 1:
                overlapSkipCntBA += 1
                continue
            okCntBA += 1
            #now same the hit scores
            hitId = '%s!%s'%(q, s)
            hitIdRev = '%s!%s'%(s, q)
            # add sequence lengths in dictionaries
            if not q in betweenLenDictB:
                betweenLenDictB[q] = qlen
            if not s in betweenLenDictA:
                betweenLenDictA[s] = slen
            #save the score
            scoreBA[hitId] = score
            #if hitRev is not present in AB
            if not hitIdRev in scoreAB:
                scoreAB[hitIdRev] = scoreCoff
            #add match and scores for each query sequence
            if not q in hitsBinA:
                hitsBinA[q] = OrderedDict()
            hitsBinA[q][s] = score

    # sort the AB hits by best score
    for query in hitsAinB:
        tmpDict = hitsAinB[query]
        if len(tmpDict) == 1:
            continue
        #update with the sorted ditionary
        tplList = [(k, tmpDict[k]) for k in sorted(tmpDict, key=tmpDict.get, reverse=True)]
        tmpDict = OrderedDict()
        for tpl in tplList:
            tmpDict[tpl[0]] = tpl[1]
        hitsAinB[query] = tmpDict
    # sort the BA hits by best score
    for query in hitsBinA:
        tmpDict = hitsBinA[query]
        if len(tmpDict) == 1:
            continue
        #update with the sorted ditionary
        tplList = [(k, tmpDict[k]) for k in sorted(tmpDict, key=tmpDict.get, reverse=True)]
        tmpDict = OrderedDict()
        for tpl in tplList:
            tmpDict[tpl[0]] = tpl[1]
        hitsBinA[query] = tmpDict
    if debug:
        print(f"Loaded sequence lengths for A:\t{len(betweenLenDictA)}")
        print(f"Loaded sequence lengths for B:\t{len(betweenLenDictB)}")
        print(f"\nLoaded hits AB:\t{len(scoreAB)}")
        print(f"Query sequences in A with orthologs in B:\t{len(hitsAinB)}")
        print(f"Overlap fail AB:\t{overlapSkipCntAB}")
        print(f"Low score AB:\t{lowScoreCntAB}")
        print(f"OK alignments AB:\t{okCntAB}")
        print(f"\nLoaded hits BA:\t{len(scoreBA)}")
        print(f"Query sequences in B with orthologs in A:\t{len(hitsBinA)}")
        print(f"Overlap fail BA:\t{overlapSkipCntBA}")
        print(f"Low score BA:\t{lowScoreCntBA}")
        print(f"OK alignments BA:\t{okCntBA}")
    #return the dictionaries
    return (scoreAB, hitsAinB, scoreBA, hitsBinA, betweenLenDictA, betweenLenDictB)



''' # This function is not used anymore and could be removed in the future
def load_within_proteomes_scores_fast(alignFileAA, alignFileBB, ortoA, ortoB, lenDictA, lenDictB, covCoff=0.25, overlapCoff=0.5, scoreCoff=40, debug=False):
    """Load within proteomes scores for AA and BB alignments (Cython)."""
    if debug:
        print('\nload_within_proteomes_scores_fast (Cython) :: START')
        print('Input AA: %s'%alignFileAA)
        print('Input BA: %s'%alignFileBB)
        print('Sequence lengths pre-loaded fo A: {:d}'.format(len(lenDictA)))
        print('Sequence lengths pre-loaded fo B: {:d}'.format(len(lenDictB)))
        print('Coverage cutoff: %s'%str(covCoff))
        print('Overlap cutoff: %s'%str(overlapCoff))
        print('Overlap cutoff: %s'%str(scoreCoff))
    if not os.path.isfile(alignFileAA):
        sys.stderr.write('The file %s was not found, please provide a valid input path'%alignFileAA)
        sys.exit(-2)
    if not os.path.isfile(alignFileBB):
        sys.stderr.write('The file %s was not found, please provide a valid input path'%alignFileBB)
        sys.exit(-2)

    #create the dictionaries to store the ids and scores
    #maxMatchCnt = 1 #will stote the maximum number hit for all the processed alignments
    scoreAA = OrderedDict()
    scoreBB = OrderedDict()
    hitsAinA = OrderedDict()
    hitsBinB = OrderedDict()

    # define file names and file descriptor pointer in C
    filename_byte_string = alignFileAA.encode("UTF-8")
    cdef char* alignFileAAc = filename_byte_string
    # convert the second input file name to bytestring
    filename_byte_string = alignFileBB.encode("UTF-8")
    cdef char* alignFileBBc = filename_byte_string
    #file pointer
    cdef FILE* cfile
    # varibales for files and lines
    cdef char * line = NULL
    cdef size_t l = 0
    cdef ssize_t read

    # define the variables that will be used
    cdef int qlen, slen, qAggrMatch, sAggrMatch, qLocMatch, sLocMatch, maxMatchCnt, lnCntAA, overlapSkipCntAA, lowScoreCntAA, okCntAA, isNotOrtoA

    cdef float score, overlapCoff_c, scoreCoff_c, covCoff_c
    covCoff_c = <float>covCoff
    scoreCoff_c = <float>scoreCoff
    overlapCoff_c = <float>overlapCoff
    #initialize counters
    lnCntAA = 0
    overlapSkipCntAA = 0
    lowScoreCntAA = 0
    okCntAA = 0
    isNotOrtoA = 0

    #open the alignments for AA
    cfile = fopen(alignFileAAc, "rb")
    if cfile == NULL:
        raise FileNotFoundError(2, "No such file or directory: '%s'" % alignFileAAc)
    # read the file and load hits for AA
    while True:
        read = getline(&line, &l, cfile)
        if read == -1:
            break
        lnCntAA += 1
        #split the string
        flds = line.split(b'\t', 8)

        # convert bytes to strings
        #use cfuntions for convertions to int and float
        q = flds[0].decode()
        #print(q)
        s = flds[1].decode()
        #print(s)
        score = atof(flds[2])
        qlen = atoi(flds[3])
        slen = atoi(flds[4])
        qAggrMatch = atoi(flds[5])
        sAggrMatch = atoi(flds[6])
        qLocMatch = atoi(flds[7])
        sLocMatch = atoi(flds[8])

        #check if the alignment should be used
        if score < scoreCoff_c:
            lowScoreCntAA += 1
            continue
        #skip if there if there an ortholog associated to the corresponding query sequence
        if q not in ortoA:
            isNotOrtoA += 1
            continue
        if overlap_test_c(qlen, slen, qAggrMatch, sAggrMatch, qLocMatch, sLocMatch, covCoff_c, overlapCoff_c) == 1:
            overlapSkipCntAA += 1
            continue
        okCntAA += 1
        #now add the hit and its score to the corresponding dictionaries
        hitId = '%s!%s'%(q, s)
        # add sequence lengths in dictionary
        if not q in lenDictA:
          lenDictA[q] = qlen
        if q != s:
          if not s in lenDictA:
            lenDictA[s] = slen
        #save the score
        scoreAA[hitId] = int(round(score, 0))
        #add match and scores for each query sequence
        if not q in hitsAinA:
            hitsAinA[q] = OrderedDict()
        hitsAinA[q][s] = int(round(score, 0))

    #close input file
    fclose(cfile)

    # define the variables that will be used for BB
    cdef int lnCntBB, overlapSkipCntBB, lowScoreCntBB, okCntBB, isNotOrtoB

    #initialize counters
    lnCntBB = 0
    overlapSkipCntBB = 0
    lowScoreCntBB = 0
    okCntBB = 0
    isNotOrtoB = 0

    #open the alignments for BB
    cfile = fopen(alignFileBBc, "rb")
    if cfile == NULL:
        raise FileNotFoundError(2, "No such file or directory: '%s'" % alignFileBBc)
    # read the file and load hits for AA
    while True:
        read = getline(&line, &l, cfile)
        if read == -1:
            break
        lnCntBB += 1
        #split the string
        flds = line.split(b'\t', 8)
        # convert bytes to strings
        #use cfuntions for convertions to int and float
        q = flds[0].decode()
        s = flds[1].decode()
        score = atof(flds[2])
        qlen = atoi(flds[3])
        slen = atoi(flds[4])
        qAggrMatch = atoi(flds[5])
        sAggrMatch = atoi(flds[6])
        qLocMatch = atoi(flds[7])
        sLocMatch = atoi(flds[8])

        #check if the alignment should be used
        if score < scoreCoff_c:
            lowScoreCntBB += 1
            continue
        #skip if there if there an ortholog associated to the corresponding query sequence
        if q not in ortoB:
            isNotOrtoB += 1
            continue
        if overlap_test_c(qlen, slen, qAggrMatch, sAggrMatch, qLocMatch, sLocMatch, covCoff_c, overlapCoff_c) == 1:
            overlapSkipCntBB += 1
            continue
        okCntBB += 1
        #now add the hit and its score to the corresponding dictionaries
        hitId = '%s!%s'%(q, s)
        # add sequence lengths in dictionary
        if not q in lenDictB:
          lenDictB[q] = qlen
        if q != s:
          if not s in lenDictB:
            lenDictB[s] = slen
        #save the score
        scoreBB[hitId] = int(round(score, 0))
        #add match and scores for each query sequence
        if not q in hitsBinB:
            hitsBinB[q] = OrderedDict()
        hitsBinB[q][s] = int(round(score, 0))

    #close input file
    fclose(cfile)
    #print some debug lines
    if debug:
        print('Sequence lengths loaded fo A: {:d}'.format(len(lenDictA)))
        print('Sequence lengths loaded fo B: {:d}'.format(len(lenDictB)))
        print('\nSummary from analysis of within alignment:\t%s'%alignFileAA)
        print('Reads lines from AA:\t%d'%lnCntAA)
        print('Loaded hits for AA:\t%d'%len(scoreAA))
        print('Low score AA:\t%d'%lowScoreCntAA)
        print('Not a ortholog:\t%d'%isNotOrtoA)
        print('Overlap fail AA:\t%d'%overlapSkipCntAA)
        print('OK alingments AA:\t%d'%okCntAA)
        print('Query from A with hits in A:\t%d'%len(list(hitsAinA.keys())))
        print('\nSummary from analysis of within alignment:\t%s'%alignFileBB)
        print('Reads lines from BB:\t%d'%lnCntBB)
        print('Loaded hits for BB:\t%d'%len(scoreBB))
        print('Low score BB:\t%d'%lowScoreCntBB)
        print('Not a ortholog:\t%d'%isNotOrtoB)
        print('Overlap fail BB:\t%d'%overlapSkipCntBB)
        print('OK alingments BB:\t%d'%okCntBB)
        print('Query from B with hits in B:\t%d'%len(list(hitsBinB.keys())))
        #print('Max maches count for AA and BB:\t%d'%maxMatchCnt)
    # return dictionaries
    return (scoreAA, hitsAinA, scoreBB, hitsBinB, lenDictA, lenDictB)
'''


# DEBUG-FUNCTION: this should be removed in future releases
'''
def load_within_proteomes_scores_single(alignFileAA, ortoA, lenDictA, covCoff=0.25, overlapCoff=0.5, scoreCoff=40, debug=False):
    """Load within proteomes scores for AA and BB alignments (Cython)."""
    if debug:
        printf('\nload_within_proteomes_scores_single (Cython) :: START')
        print('Input AA: %s'%alignFileAA)
        print('Sequence lengths pre-loaded for A: {:d}'.format(len(lenDictA)))
        print('Coverage cutoff: %s'%str(covCoff))
        print('Overlap cutoff: %s'%str(overlapCoff))
        print('Overlap cutoff: %s'%str(scoreCoff))
    if not os.path.isfile(alignFileAA):
        sys.stderr.write('The file %s was not found, please provide a valid input path'%alignFileAA)
        sys.exit(-2)

    #create the dictionaries to store the ids and scores
    scoreAA = OrderedDict()
    hitsAinA = OrderedDict()

    # define file names and file descriptor pointer in C
    filename_byte_string = alignFileAA.encode("UTF-8")
    cdef char* alignFileAAc = filename_byte_string
    #file pointer
    cdef FILE* cfile
    # varibales for files and lines
    cdef char * line = NULL
    cdef size_t l = 0
    cdef ssize_t read

    # define the variables that will be used
    cdef int qlen, slen, qAggrMatch, sAggrMatch, qLocMatch, sLocMatch, maxMatchCnt, lnCntAA, overlapSkipCntAA, lowScoreCntAA, okCntAA, isNotOrtoA

    cdef float score, overlapCoff_c, scoreCoff_c, covCoff_c
    covCoff_c = <float>covCoff
    scoreCoff_c = <float>scoreCoff
    overlapCoff_c = <float>overlapCoff
    #initialize counters
    lnCntAA = 0
    overlapSkipCntAA = 0
    lowScoreCntAA = 0
    okCntAA = 0
    isNotOrtoA = 0

    #open the alignments for AA
    cfile = fopen(alignFileAAc, "rb")
    if cfile == NULL:
        raise FileNotFoundError(2, "No such file or directory: '%s'" % alignFileAAc)
    # read the file and load hits for AA
    while True:
        read = getline(&line, &l, cfile)
        if read == -1:
            break
        lnCntAA += 1
        #split the string
        flds = line.split(b'\t', 8)

        # convert bytes to strings
        #use cfuntions for convertions to int and float
        q = flds[0].decode()
        #print(q)
        s = flds[1].decode()
        #print(s)
        score = atof(flds[2])
        qlen = atoi(flds[3])
        slen = atoi(flds[4])
        qAggrMatch = atoi(flds[5])
        sAggrMatch = atoi(flds[6])
        qLocMatch = atoi(flds[7])
        sLocMatch = atoi(flds[8])

        #check if the alignment should be used
        if score < scoreCoff_c:
            lowScoreCntAA += 1
            continue
        #skip if there is an ortholog associated to the corresponding query sequence
        if q not in ortoA:
            isNotOrtoA += 1
            continue
        if overlap_test_c(qlen, slen, qAggrMatch, sAggrMatch, qLocMatch, sLocMatch, covCoff_c, overlapCoff_c) == 1:
            overlapSkipCntAA += 1
            continue
        okCntAA += 1
        #now add the hit and its score to the corresponding dictionaries
        hitId = '%s!%s'%(q, s)
        # add sequence lengths in dictionary
        if not q in lenDictA:
          lenDictA[q] = qlen
        if q != s:
          if not s in lenDictA:
            lenDictA[s] = slen
        #save the score
        scoreAA[hitId] = int(round(score, 0))
        #add match and scores for each query sequence
        if not q in hitsAinA:
            hitsAinA[q] = OrderedDict()
        hitsAinA[q][s] = int(round(score, 0))

    #close input file
    fclose(cfile)

    #print some debug lines
    if debug:
        print('Sequence lengths loaded fo A: {:d}'.format(len(lenDictA)))
        print('\nSummary from analysis of within alignment:\t%s'%alignFileAA)
        print('Reads lines from AA:\t%d'%lnCntAA)
        print('Loaded hits for AA:\t%d'%len(scoreAA))
        print('Low score AA:\t%d'%lowScoreCntAA)
        print('Not a ortholog:\t%d'%isNotOrtoA)
        print('Overlap fail AA:\t%d'%overlapSkipCntAA)
        print('OK alignments AA:\t%d'%okCntAA)
        print('Query from A with hits in A:\t%d'%len(list(hitsAinA.keys())))
    # return dictionaries
    return (scoreAA, hitsAinA, lenDictA)
'''



def preprocess_within_align(alignFileAA, lenDictA, covCoff=0.25, overlapCoff=0.5, scoreCoff=40, debug=False) -> Tuple[Dict[str, int], Dict[str, int]]:
    """Load within proteomes scores for AA and BB alignments (Cython)."""
    if debug:
        print("\npreprocess_within_align (Cython) :: START")
        print(f"Input AA: {alignFileAA}")
        print(f"Coverage cutoff: {covCoff}")
        print(f"Overlap cutoff: {overlapCoff}")
        print(f"Overlap cutoff: {scoreCoff}")
    if not os.path.isfile(alignFileAA):
        sys.stderr.write(f"The file {alignFileAA} was not found, please provide a valid input path")
        sys.exit(-2)

    #create the dictionaries to store the ids and scores
    # Will contain the score for each query-subject pair
    withinAlignDict:Dict[str, int] = {}

    # define file names and file descriptor pointer in C
    filename_byte_string = alignFileAA.encode("UTF-8")
    cdef char* alignFileAAc = filename_byte_string
    #file pointer
    cdef FILE* cfile
    # varibales for files and lines
    cdef char * line = NULL
    cdef size_t l = 0
    cdef ssize_t read

    # define the variables that will be used
    cdef int qlen, slen, qAggrMatch, sAggrMatch, qLocMatch, sLocMatch, maxMatchCnt, lnCntAA, overlapSkipCntAA, lowScoreCntAA, okCntAA, isNotOrtoA

    cdef float score, overlapCoff_c, scoreCoff_c, covCoff_c
    covCoff_c = <float>covCoff
    scoreCoff_c = <float>scoreCoff
    overlapCoff_c = <float>overlapCoff
    #initialize counters
    lnCntAA:int = 0
    overlapSkipCntAA:int = 0
    lowScoreCntAA:int = 0
    okCntAA:int = 0
    isNotOrtoA:int = 0
    q:str = ""
    s:str = ""
    hitId:str = ""

    #open the alignments for AA
    cfile = fopen(alignFileAAc, "rb")
    if cfile == NULL:
        raise FileNotFoundError(2, f"No such file or directory: '{alignFileAAc}'")
    # read the file and load hits for AA
    while True:
        read = getline(&line, &l, cfile)
        if read == -1:
            break
        lnCntAA += 1
        #split the string
        flds = line.split(b"\t", 8)

        # convert bytes to strings
        #use cfuntions for convertions to int and float
        q = flds[0].decode()
        #print(q)
        s = flds[1].decode()
        #print(s)
        score = atof(flds[2])
        qlen = atoi(flds[3])
        slen = atoi(flds[4])
        qAggrMatch = atoi(flds[5])
        sAggrMatch = atoi(flds[6])
        qLocMatch = atoi(flds[7])
        sLocMatch = atoi(flds[8])

        #check if the alignment should be used
        '''
        if score < scoreCoff_c:
            lowScoreCntAA += 1
            continue
        '''
        #skip if there is an ortholog associated to the corresponding query sequence
        '''
        if q not in ortoA:
            isNotOrtoA += 1
            continue
        '''
        if overlap_test_c(qlen, slen, qAggrMatch, sAggrMatch, qLocMatch, sLocMatch, covCoff_c, overlapCoff_c) == 1:
            overlapSkipCntAA += 1
            continue
        okCntAA += 1
        #now add the hit and its score to the corresponding dictionaries
        hitId = f"{q}!{s}"

        if not hitId in withinAlignDict:
          withinAlignDict[hitId] = int(round(score, 0))

        # add sequence lengths in dictionary
        if not q in lenDictA:
            lenDictA[q] = qlen
        if q != s:
            if not s in lenDictA:
                lenDictA[s] = slen

    #close input file
    fclose(cfile)

    #print some debug lines
    if debug:
        print(f"\nSummary from preprocessing of within alignment:\t{alignFileAA}")
        print(f"Reads lines from AA:\t{lnCntAA}")
        print(f"Sequence lengths loaded for A:\t{len(lenDictA)}")
        print(f"Overlap fail AA:\t{overlapSkipCntAA}")
        print(f"Low score AA:\t{lowScoreCntAA}")
        print(f"Entries in within-alignment dict:\t{len(withinAlignDict)}")
    # return dictionaries
    return (withinAlignDict, lenDictA)



def preprocess_within_align_compressed(alignFileAA, lenDictA, covCoff=0.25, overlapCoff=0.5, scoreCoff=40, debug=False) -> Tuple[Dict[str, int], Dict[str, int]]:
    """Load within-proteome scores for AA and BB alignments from a compressed text file."""
    import gzip
    if debug:
        print("\npreprocess_within_align_compressed :: START")
        print(f"Input AA: {alignFileAA}")
        print(f"Coverage cutoff: {covCoff}")
        print(f"Overlap cutoff: {overlapCoff}")
        print(f"Overlap cutoff: {scoreCoff}")
    if not os.path.isfile(alignFileAA):
        sys.stderr.write(f"The file {alignFileAA} was not found, please provide a valid input path")
        sys.exit(-2)

    #create the dictionaries to store the ids and scores
    # Will contain the score for each query-subject pair
    withinAlignDict:Dict[str, int] = {}

    # define the variables that will be used
    cdef int qlen, slen, qAggrMatch, sAggrMatch, qLocMatch, sLocMatch, maxMatchCnt, lnCntAA, overlapSkipCntAA, lowScoreCntAA, okCntAA, isNotOrtoA
    cdef float score, overlapCoff_c, scoreCoff_c, covCoff_c
    covCoff_c = <float>covCoff
    scoreCoff_c = <float>scoreCoff
    overlapCoff_c = <float>overlapCoff
    #initialize counters
    lnCntAA:int = 0
    overlapSkipCntAA:int = 0
    lowScoreCntAA:int = 0
    okCntAA:int = 0
    isNotOrtoA:int = 0
    line:bytes = bytes()
    q:str = s = hitId =""

    # read the file and load hits for AA
    with gzip.open(alignFileAA, "rb") as gzifd:
        for line in gzifd.readlines():
            lnCntAA += 1
            #split the string
            flds = line.split(b'\t', 8)
            # convert bytes to strings
            #use cfuntions for convertions to int and float
            q = flds[0].decode()
            #print(q)
            s = flds[1].decode()
            #print(s)
            score = atof(flds[2])
            qlen = atoi(flds[3])
            slen = atoi(flds[4])
            qAggrMatch = atoi(flds[5])
            sAggrMatch = atoi(flds[6])
            qLocMatch = atoi(flds[7])
            sLocMatch = atoi(flds[8])

            #check if the alignment should be used
            '''
            if score < scoreCoff_c:
                lowScoreCntAA += 1
                continue
            '''
            #skip if there is an ortholog associated to the corresponding query sequence
            '''
            if q not in ortoA:
                isNotOrtoA += 1
                continue
            '''
            if overlap_test_c(qlen, slen, qAggrMatch, sAggrMatch, qLocMatch, sLocMatch, covCoff_c, overlapCoff_c) == 1:
                overlapSkipCntAA += 1
                continue
            okCntAA += 1
            #now add the hit and its score to the corresponding dictionaries
            hitId = f"{q}!{s}"

            if not hitId in withinAlignDict:
                withinAlignDict[hitId] = int(round(score, 0))

            # add sequence lengths in dictionary
            if not q in lenDictA:
                lenDictA[q] = qlen
            if q != s:
                if not s in lenDictA:
                    lenDictA[s] = slen

    #print some debug lines
    if debug:
        print(f"\nSummary from preprocessing of within alignment:\t{alignFileAA}")
        print(f"Reads lines from AA:\t{lnCntAA}")
        print(f"Sequence lengths loaded for A:\t{len(lenDictA)}")
        print(f"Overlap fail AA:\t{overlapSkipCntAA}")
        print(f"Low score AA:\t{lowScoreCntAA}")
        print(f"Entries in within-alignment dict:\t{len(withinAlignDict)}")
    # return dictionaries
    return (withinAlignDict, lenDictA)


'''
def overlap_test(qlen, slen, qAggrMatch, sAggrMatch, qLocMatch, sLocMatch, coverageCutoff, overlapCutoff,  debug=False):
    """Filter out fragmentary hits."""
    # Filter out fragmentary hits by:
    # Ignore hit if aggregate matching area covers less than overlapCutoff of sequence.
    # Ignore hit if local matching segments cover less than coverageCutoff of sequence.
    #
    # qlen and slen are query and subject lengths, respectively
    # qAggrMatch and sAggrMatch are lengths of the aggregate matching region on query and subject. (From start of first matching segment to end of last matching segment).
    # qLocMatch and sLocMatch are local matching length on query and subject, (Sum of all segments length's on query [and subject]), respectively.
    # The above variables are respectively are found at positions 3-7 of parsed blast output lines
    #if qlen >= slen:
    if qAggrMatch < float(overlapCutoff * qlen):
        return False
    if qLocMatch < float(coverageCutoff * qlen):
        return False
    #else:
    if sAggrMatch < float(overlapCutoff * slen):
        return False
    if sLocMatch < float(coverageCutoff * slen):
        return False
    return True
'''


#write the overlap check in C
cdef int overlap_test_c(int qlen, int slen, int qAggrMatch, int sAggrMatch, int qLocMatch, int sLocMatch, float coverageCutoff, float overlapCutoff):
  """Check overlap (Cython)"""
  """Filter out fragmentary hits."""
  # Filter out fragmentary hits by:
  # Ignore hit if aggregate matching area covers less than overlapCutoff of sequence.
  # Ignore hit if local matching segments cover less than coverageCutoff of sequence.
  #
  # qlen and slen are query and subject lengths, respectively
  # qAggrMatch and sAggrMatch are lengths of the aggregate matching region on query and subject. (From start of first  matching segment to end of last matching segment).
  # qLocMatch and sLocMatch are local matching length on query and subject, (Sum of all segments length's on query [and  subject]), respectively.
  # The above variables are respectively are found at positions 3-7 of parsed blast output lines

  # 1: overlap present (the alignment should be skipped)
  # 0: no overlap (the alignment can be used)
  if qAggrMatch < overlapCutoff * qlen:
      return 1
  if qLocMatch < coverageCutoff * qlen:
      return 1
  if sAggrMatch < overlapCutoff * slen:
      return 1
  if sLocMatch < coverageCutoff * slen:
      return 1
  return 0



def rewrite_clusters_c(inTbl: str, mergedClstrs: List[str], mergedIds: List[str], skipDict: Dict[str, None], debug: bool=False) -> str:
    """Write down merged cluster of ortholog relationships."""
    if debug:
        print("\nrewrite_clusters_c :: START")
        print(f"Table path: {inTbl}")
        print(f"Merged clusters:\t{len(mergedClstrs)}")
        print(f"Merged cluster IDs:\t{len(mergedIds)}")
        print(f"IDs to be skipped:\t{len(skipDict)}")

    if not os.path.isfile(inTbl):
        sys.stderr.write("\nERROR: the ortholog table\n{:s}\nwas not found.".format(inTbl))
        sys.exit(-2)

    # extract the pair name
    # original tables name must be like "table.sp1-sp2.sorted"
    pairName = os.path.basename(inTbl).split(".", 2)[1]

    # find the main table and matrixes directories
    tblDir: str = os.path.dirname(inTbl)
    if not os.path.isdir(tblDir):
        sys.stderr.write(f"\nERROR: the directory with ortholog tables\n{tblDir}\nwas not found.")
        sys.exit(-2)

    # define the output paths
    outTbl: str = os.path.join(tblDir, f"table.{pairName}")
    tmpTbl: str = os.path.join(tblDir, f"table.{pairName}.tmp")
    # sys.exit("DEBUG@inpyranoid_c.pyx -> rewrite_clusters_c")

    # other variables
    cdef int rdCnt
    rdCnt = 0
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

    #open the pairwise ortholog table
    cfile = fopen(inTbl_c, "rb")
    if cfile == NULL:
        raise FileNotFoundError(2, f"No such file or directory: '{inTbl_c}'")

    # example of line to be parsed
    # 25	64	1.1110 0.051 1.943 1.0	2.16 1.0 2.653 0.18

    # open the temporary table
    ofdTmp = open(tmpTbl, "wt")
    # write the header
    ofdTmp.write("Score\tOrtoA\tOrtoB\n")

    while True:
        read = getline(&line, &l, cfile)
        if read == -1:
            break

        # split the binary stream
        flds = line.split(b"\t", 1)
        clstrId = flds[0].decode()
        # if the first letter is a 'O' then it is the cluster headers
        if clstrId[0] == "O":
          # skip header
          continue
        rdCnt += 1
        rxPart: str = flds[1].decode()
        if clstrId in skipDict:
            continue
        if not clstrId in mergedIds:
            ofdTmp.write(rxPart)

    # now write the merged clusters in the new table
    while len(mergedClstrs) > 0:
        ofdTmp.write(mergedClstrs.pop())

    # close the files
    fclose(cfile)
    ofdTmp.close()
    # remove input table
    os.remove(inTbl)

    # load the new table using pandas and sort it by clstr score
    df = pd.read_csv(tmpTbl, sep='\t')
    # sort the dataframe by score
    dfSorted = df.sort_values('Score', ascending=False, inplace=False)
    del df
    # sort the table by cluster score
    tmpSorted: str = tmpTbl.replace('.tmp', '.sorted')
    dfSorted.to_csv(tmpSorted, sep='\t', header=False, index=False)
    # remove not required files
    os.remove(tmpTbl)
    # set final path
    finalTblPath: str = os.path.join(tblDir, f"table.{pairName}")
    # define file names and file descriptor pointer in C
    filename_byte_string = tmpSorted.encode("UTF-8")
    inTbl_c = filename_byte_string

    # write the final ortholog table
    ofd = open(finalTblPath, 'wt')
    ofd.write("OrtoId\tScore\tOrtoA\tOrtoB\n")
    rdCnt = 0

    #open the pairwise ortholog table
    cfile = fopen(inTbl_c, "rb")
    if cfile == NULL:
        raise FileNotFoundError(2, f"No such file or directory: '{inTbl_c}'")

    while True:
        read = getline(&line, &l, cfile)
        if read == -1:
            break
        rdCnt += 1
        ofd.write(f"{rdCnt}\t{line.decode()}")

    # close files
    fclose(cfile)
    ofd.close()
    # remove sorted file
    os.remove(tmpSorted)
    return finalTblPath



def write_sql_c(inTbl: str, outDir: str=os.getcwd(), debug: bool=False) -> str:
    """Load ortholog relationships and generate SQl table."""
    if debug:
        print("\nwrite_sql_c :: START")
        print(f"Table path: {inTbl}")
        print(f"Output directory: {outDir}")

    if not os.path.isfile(inTbl):
        sys.stderr.write(f"\nERROR: the ortholog table\n{inTbl}\nwas not found.")
        sys.exit(-2)

    # extract the pair name
    # original tables must be named like "table.sp1-sp2"
    pairName: str = os.path.basename(inTbl).split(".", 1)[1]
    sp1: str = ""
    sp2: str = ""
    # extract the species
    sp1, sp2 = pairName.split("-", 1)

    # define the output paths
    outSql: str = os.path.join(outDir, "sqltable.{:s}".format(pairName))
    # other variables
    cdef int rdCnt
    rdCnt = 0
    tmpSc: float = 0.
    clstrId: str = ""
    outSqlLnStart: str = ""
    # define file names and file descriptor pointer in C
    filename_byte_string = inTbl.encode("UTF-8")
    cdef char* inTbl_c = filename_byte_string
    #file pointer
    cdef FILE* cfile
    # varibales for files and lines
    cdef char * line = NULL
    cdef size_t l = 0
    cdef ssize_t read

    #open the pairwise ortholog table
    cfile = fopen(inTbl_c, "rb")
    if cfile == NULL:
        raise FileNotFoundError(2, f"No such file or directory: '{inTbl_c}'")

    # example of line to be parsed
    # 25	64	1.1110 0.051 1.943 1.0	2.16 1.0 2.653 0.18

    # create the SQL table
    ofdSql = open(outSql, "wt")

    while True:
        read = getline(&line, &l, cfile)
        if read == -1:
            break

        # split the binary stream
        flds = line.rstrip(b"\n").rsplit(b"\t", 3)
        clstrId = flds[0].decode()
        # if the first letter is a 'O' then it is the cluster headers
        if clstrId[0] == "O":
          # skip the header
          continue
        rdCnt += 1
        # write the starting part of the SQL entry
        outSqlLnStart = f"{clstrId}\t{flds[1].decode()}"

        # example of SQL entries for a 4 genes cluster (3 orthologs from Sp1)
        # 66	320	1	0.094	1.1396
        # 66	320	1	0.116	1.1522
        # 66	320	1	1.0	1.492
        # 66	320	2	1.0	2.163

        # split left part of the cluster
        tmpSplit = flds[2].split(b" ")
        # write genes from Sp1 in SQL file
        for i, el in enumerate(tmpSplit):
          # if it is the gene part
          if i % 2 == 0:
              ofdSql.write('{:s}\t{:s}\t{:s}\t{:s}\n'.format(outSqlLnStart, sp1, tmpSplit[i + 1].decode(), el.decode()))

        # split right part of the cluster
        tmpSplit = flds[3].split(b" ")
        # write genes from Sp2 in SQL file
        for i, el in enumerate(tmpSplit):
          # if it is the gene part
          if i % 2 == 0:
              ofdSql.write('{:s}\t{:s}\t{:s}\t{:s}\n'.format(outSqlLnStart, sp2, tmpSplit[i + 1].decode(), el.decode()))

    # close the SQL file
    ofdSql.close()
    return outSql
