#!/usr/bin/env python
"""
Baseline system for the CoNLL-SIGMORPHON 2018 Shared Task 1.

Author: Mans Hulden
Last Update: 04/21/2018
"""

from __future__ import print_function
import sys, codecs, os, string, getopt, re
from functools import wraps

def hamming(s,t):
    return sum(1 for x,y in zip(s,t) if x != y)    

def halign(s,t):
    """Align two strings by Hamming distance."""
    slen = len(s)
    tlen = len(t)    
    minscore = len(s) + len(t) + 1
    for upad in xrange(0, len(t)+1):
        upper = '_' * upad + s + (len(t) - upad) * '_'
        lower = len(s) * '_' + t
        score = hamming(upper, lower)
        if score < minscore:
            bu = upper
            bl = lower
            minscore = score

    for lpad in xrange(0, len(s)+1):
        upper = len(t) * '_' + s
        lower = (len(s) - lpad) * '_' + t + '_' * lpad
        score = hamming(upper, lower)
        if score < minscore:
            bu = upper
            bl = lower
            minscore = score

    zipped = zip(bu,bl)
    newin  = ''.join(i for i,o in zipped if i != '_' or o != '_')
    newout = ''.join(o for i,o in zipped if i != '_' or o != '_')
    return newin, newout

def levenshtein(s, t, inscost = 1.0, delcost = 1.0, substcost = 1.0):
    """Recursive implementation of Levenshtein, with alignments returned."""
    @memolrec
    def lrec(spast, tpast, srem, trem, cost):
        if len(srem) == 0:
            return spast + len(trem) * '_', tpast + trem, '', '', cost + len(trem)
        if len(trem) == 0:
            return spast + srem, tpast + len(srem) * '_', '', '', cost + len(srem)

        addcost = 0
        if srem[0] != trem[0]:
            addcost = substcost
            
        return min((lrec(spast + srem[0], tpast + trem[0], srem[1:], trem[1:], cost + addcost),
                   lrec(spast + '_', tpast + trem[0], srem, trem[1:], cost + inscost),
                   lrec(spast + srem[0], tpast + '_', srem[1:], trem, cost + delcost)),
                   key = lambda x: x[4])

    answer = lrec('', '', s, t, 0)
    return answer[0],answer[1],answer[4]

def memolrec(func):
    """Memoizer for Levenshtein."""
    cache = {}
    @wraps(func)
    def wrap(sp, tp, sr, tr, cost):
        if (sr,tr) not in cache:
            res = func(sp, tp, sr, tr, cost)
            cache[(sr,tr)] = (res[0][len(sp):], res[1][len(tp):], res[4] - cost)
        return sp + cache[(sr,tr)][0], tp + cache[(sr,tr)][1], '', '', cost + cache[(sr,tr)][2]
    return wrap
    
def alignprs(lemma, form):
    """Break lemma/form into three parts:
    IN:  1 | 2 | 3
    OUT: 4 | 5 | 6
    1/4 are assumed to be prefixes, 2/5 the stem, and 3/6 a suffix.
    1/4 and 3/6 may be empty.
    """
    
    al = levenshtein(lemma, form, substcost = 1.1) # Force preference of 0:x or x:0 by 1.1 cost
    alemma, aform = al[0], al[1]
    # leading spaces
    lspace = max(len(alemma) - len(string.lstrip(alemma, '_')), len(aform) - len(string.lstrip(aform,'_')))
    # trailing spaces
    tspace = max(len(alemma[::-1]) - len(string.lstrip(alemma[::-1],'_')), len(aform[::-1]) - len(string.lstrip(aform[::-1],'_')))
    return alemma[0:lspace], alemma[lspace:len(alemma)-tspace], alemma[len(alemma)-tspace:], aform[0:lspace], aform[lspace:len(alemma)-tspace], aform[len(alemma)-tspace:]

def prefix_suffix_rules_get(lemma, form):
    """Extract a number of suffix-change and prefix-change rules
    based on a given example lemma+inflected form."""
    lp,lr,ls,fp,fr,fs = alignprs(lemma, form) # Get six parts, three for in three for out

    # Suffix rules
    ins  = lr + ls + ">"
    outs = fr + fs + ">"    
    srules = set()
    for i in xrange(min(len(ins), len(outs))):
        srules.add((ins[i:], outs[i:]))
    srules = {(string.replace(x[0], '_',''), string.replace(x[1],'_','')) for x in srules}

    # Prefix rules
    prules = set()
    if len(lp) >= 0 or len(fp) >= 0:
        inp = "<" + lp
        outp = "<" + fp
        for i in xrange(0,len(fr)):
            prules.add((inp + fr[:i],outp + fr[:i]))
            prules = {(string.replace(x[0],'_',''), string.replace(x[1], '_','')) for x in prules}

    return prules, srules

def apply_best_rule(lemma, msd, allprules, allsrules):
    """Applies the longest-matching suffix-changing rule given an input
    form and the MSD. Length ties in suffix rules are broken by frequency.
    For prefix-changing rules, only the most frequent rule is chosen."""
    
    bestrulelen = 0
    base = "<" + lemma + ">"
    if msd not in allprules and msd not in allsrules:
        return lemma # Haven't seen this inflection, so bail out

    if msd in allsrules:
        applicablerules = [(x[0],x[1],y) for x,y in allsrules[msd].iteritems() if x[0] in base]
        if applicablerules:
            bestrule = max(applicablerules, key = lambda x: (len(x[0]), x[2], len(x[1])))           
            base = string.replace(base, bestrule[0], bestrule[1])
        
    if msd in allprules:
        applicablerules = [(x[0],x[1],y) for x,y in allprules[msd].iteritems() if x[0] in base]
        if applicablerules:
            bestrule = max(applicablerules, key = lambda x: (x[2]))
            base = string.replace(base, bestrule[0], bestrule[1])
                
    base = string.replace(base, '<', '')
    base = string.replace(base, '>', '')
    #print(lemma,base)
    return base

def numleadingsyms(s, symbol):
    return len(s) - len(s.lstrip(symbol))
    
def numtrailingsyms(s, symbol):
    return len(s) - len(s.rstrip(symbol))


def english_rules(lemma,msd,allprules, allsrules):
    vowels = ('a', 'e', 'i', 'o', 'u')
    cons_plural = ('s', 'x', 'ch', 'sh', 'z')
    cons_list1 = ('b', 'c', 'd', 'f', 'g', 'h', 'j','k', 'l', 'm' ,'n', 'q', 'r', 's', 't', 'v', 'w', 'x', 'z')
    cons_list2 = ('p', 'g')
    cons_list3 = ('p', 'g','b','t')
    if 'V;NFIN' in msd:
        return lemma
    if 'V;3;SG;PRS' in msd:
        if lemma.endswith(cons_plural):
            return lemma + 'es'
        elif lemma.endswith('y') and lemma[-2:-1] not in vowels:
            return lemma[:-1] + 'ies'
        else:
            return lemma + 's'
    if 'V;V.PTCP;PRS' in msd:
        if lemma.endswith('e'):
            return lemma[:-1] + 'ing'
        elif lemma.endswith(cons_list3) and lemma[-2:-1] in vowels and lemma[-3:-2] not in vowels :
            return lemma + lemma[-1:] + 'ing'
        elif lemma.endswith('c'):
            return lemma + 'king'
        elif lemma.endswith('e') and lemma[-2:-1] == 'i':
            return lemma[:-2] + 'ying'        
        else:
            return lemma + 'ing'
    if 'V;V.PTCP;PST' in msd:
        if lemma.endswith('e') and lemma[-2:] != 'ee':
            return lemma + 'd'
        elif lemma.endswith('y') and lemma[-2:-1] not in vowels:
            return lemma[:-1] + 'ied'
        elif lemma.endswith(cons_list2) and lemma[-2:] != 'ng':
            return lemma + lemma[-1:] + 'ed'
        else:
            outform = apply_best_rule(lemma, msd, allprules, allsrules)
            return outform
    if 'V;PST' in msd:
        if lemma.endswith('y') and lemma[-2:-1] not in vowels:
            return lemma[:-1] + 'ied'
        elif lemma.endswith(cons_list2) and lemma[-2:] != 'ng':
            return lemma + lemma[-1:] + 'ed'
        else:
            outform = apply_best_rule(lemma, msd, allprules, allsrules)
            return outform


def german_rules(lemma,msd,allprules, allsrules):
    vowels = ('a', 'e', 'i', 'o', 'u')
    cons_list1 = ('b', 'c', 'd', 'f', 'g', 'h', 'j','k', 'l', 'm' ,'n', 'q','r', 's', 't', 'v', 'w', 'x', 'z', 'p', 'g')
    prefix = ('ab', 'zusammen', 'an', 'vor', 'herab', 'ein', 'fest', 'um', 'nach', 'zu', 'aus', 'vorher', 'weg', 'mit', 'hin')
    prefix_nonsplit = ('be', 'ver', 'ge', 'er')

    outform = apply_best_rule(lemma, msd, allprules, allsrules)
    if 'N;ACC;SG' in msd:
        return lemma
    if 'V;IND;PST;2;PL' in msd or 'V;SBJV;PRS;3;PL' in msd or 'V;IMP;2;SG' in msd or 'V;IND;PST;3;PL' in msd or 'V;IND;PRS;1;PL' in msd or 'V;IND;PRS;3;SG' in msd or 'V;IND;PST;3;SG' in msd:
        for i in prefix:
            if outform.startswith(i):
                split = len(i)
                return outform[split:] + ' ' + i
    if 'V.PTCP;PST' in msd:
        if not outform.startswith(prefix):
            return 'ge' + outform
        else:
            for i in prefix:
                if outform.startswith(i) and not outform.endswith('iert') and not outform.startswith(prefix_nonsplit):
                    split = len(i)
                    return i + 'ge' + outform[split:]
    return outform
    
    
###############################################################################

def main(argv):
    options, remainder = getopt.gnu_getopt(argv[1:], 'ohp:', ['output','help','path='])
    OUTPUT, HELP, PATH = False, False, './../all/'
    for opt, arg in options:
        if opt in ('-o', '--output'):
            OUTPUT = True
        elif opt in ('-h', '--help'):
            HELP = True
        elif opt in ('-p', '--path'):
            PATH = arg
            
    if HELP:
            print("\n*** Baseline for the CoNLL-SIGMORPHON 2018 shared task ***\n")
            print("By default, the program runs all languages")
            print("only evaluating accuracy. To create output files, use -o")
            print("The training and dev-data are assumed to live in ./../all/")
            print("Options:")
            print(" -o         create output files with guesses (and don't just evaluate)")           
            print(" -p [path]  data files path. Default is ./../all/")
            quit()
    
    for task in [1]:
        runningavgLow, runningavgMed, runningavgHigh, numiterLow, numiterMed, numiterHigh = 0.0, 0.0, 0.0, 0, 0, 0
        for lang in sorted(list({re.sub('\-train.*$','',d) for d in os.listdir(PATH) if '-train-' in d})):
            for quantity in ['high']:
                allprules, allsrules = {}, {}
                if not os.path.isfile(PATH + lang +  "-train-" + quantity):
                    continue
                lines = [line.strip() for line in codecs.open(PATH + lang + "-train-" + quantity, "r", encoding="utf-8")]

                # First, test if language is predominantly suffixing or prefixing
                # If prefixing, work with reversed strings
                prefbias, suffbias = 0,0
                for l in lines:
                    lemma, form, _ = l.split(u'\t')
                    aligned = halign(lemma, form)
                    if ' ' not in aligned[0] and ' ' not in aligned[1] and '-' not in aligned[0] and '-' not in aligned[1]:
                        prefbias += numleadingsyms(aligned[0],'_') + numleadingsyms(aligned[1],'_')
                        suffbias += numtrailingsyms(aligned[0],'_') + numtrailingsyms(aligned[1],'_')

                for l in lines: # Read in lines and extract transformation rules from pairs
                    lemma, form, msd = l.split(u'\t')
                    if prefbias > suffbias:
                        lemma = lemma[::-1]
                        form = form[::-1]
                    prules, srules = prefix_suffix_rules_get(lemma, form)
        
                    if msd not in allprules and len(prules) > 0:
                        allprules[msd] = {}
                    if msd not in allsrules and len(srules) > 0:
                        allsrules[msd] = {}

                    for r in prules:
                        if (r[0],r[1]) in allprules[msd]:
                            allprules[msd][(r[0],r[1])] = allprules[msd][(r[0],r[1])] + 1
                        else:
                            allprules[msd][(r[0],r[1])] = 1

                    for r in srules:
                        if (r[0],r[1]) in allsrules[msd]:
                            allsrules[msd][(r[0],r[1])] = allsrules[msd][(r[0],r[1])] + 1
                        else:
                            allsrules[msd][(r[0],r[1])] = 1

                # Run eval on dev
                devlines = [line.strip() for line in codecs.open(PATH + lang + "-dev", "r", encoding="utf-8")]
                numcorrect = 0
                numguesses = 0
                if OUTPUT:
                    outfile = codecs.open(PATH + lang + "-" + quantity + "-out", "w", encoding="utf-8")
                for l in devlines:
                    lemma, correct, msd, = l.split(u'\t')
                    if prefbias > suffbias:
                        lemma = lemma[::-1]
                    if lang == "english":
                        outform = english_rules(lemma, msd, allprules, allsrules)
                        if prefbias > suffbias:
                            outform = outform[::-1]
                            lemma = lemma[::-1]
                        if outform == correct:
                            numcorrect += 1
                        numguesses += 1
                        if OUTPUT:
                            outfile.write(lemma + "\t" + outform + "\t" + msd + "\n")
                    if lang == "german":
                        outform = german_rules(lemma, msd, allprules, allsrules)
                        if prefbias > suffbias:
                            outform = outform[::-1]
                            lemma = lemma[::-1]
                       # if outform != correct and lang =='german':
                           # print(outform.encode('utf8'), correct.encode('utf8'), msd)
                        if outform == correct:
                            numcorrect += 1
                        numguesses += 1
                        if OUTPUT:
                            outfile.write(lemma + "\t" + outform + "\t" + msd + "\n")
   
                if OUTPUT:
                    outfile.close()
                         
                if quantity == 'low':
                    runningavgLow += numcorrect/float(numguesses)
                    numiterLow += 1
                if quantity == 'medium':
                    runningavgMed += numcorrect/float(numguesses)
                    numiterMed += 1
                if quantity == 'high' and numguesses>0:
                    runningavgHigh += numcorrect/float(numguesses)
                    numiterHigh += 1                    
                
                print(lang + "[task " + str(task) + "/" + quantity + "]" + ": " + str(str(numcorrect/float(numguesses)))[0:7])
        #print("Average[low]:", str(runningavgLow/float(numiterLow)))
        #print("Average[medium]:", str(runningavgMed/float(numiterMed)))
        print("Average[high]:", str(runningavgHigh/float(numiterHigh)))
        print("------------------------------------\n")

if __name__ == "__main__":
    main(sys.argv)
