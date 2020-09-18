import re
import sys
from sys import argv
import string
import numpy as np
import math
'''convert input and gold to "tooo" type, where "t" stands for the start of a token,
"o" for inside of a token, white space is not counted'''

d_uni = dict()
d_bi = dict()
d_tri = dict()

lm_file = sys.argv[1]
l1 = float(sys.argv[2])
l2 = float(sys.argv[3])
l3 = float(sys.argv[4])
test_data = sys.argv[5]

output = open(sys.argv[6], 'w')

def add_eos_bos(line):
    line = line.strip("\n")
    new_line = '<s> '
    new_line = new_line + line
    new_line = new_line + ' </s>'
    return new_line
d = {}
sn = 0
oov_total = 0
word_total = 0
lg_total = 0
with open(lm_file, 'r') as f:
    for line in f:
        line = line.strip("\n")
        words = line.split(" ")
        if words[0].isdigit() is False:
            continue
        if len(words) == 4:
            d[words[3]] = float(words[1])
        if len(words) == 5:
            bigram =  words[3] + " " + words[4]
            d[bigram] = float(words[1])
        if len(words) == 6:
            trigram =  words[3] + " " + words[4] + " " + words[5]
            d[trigram] = float(words[1])
            #print(trigram,words[1])
with open(test_data, 'r') as f:
    for line in f:
        sn = sn + 1
        oov = 0
        line = add_eos_bos(line)
        output.write("Sent #" + str(sn) +": " + line + "\n")
        words = line.split(" ")
        prev_word1 = ''
        prev_word2 = ''
        order = -1
        lgprob = 0
        for word in words:
            word = word.lower()
            order = order + 1
            if len(prev_word1) != 0 and len(prev_word2) != 0:
                w3 = prev_word1 + " " + prev_word2 + " " + word
                trigram_unseen = False
                bigram_unseen = False
                unigram_unseen = False
                if w3 in d:
                    p3 = d[w3]
                else:
                    trigram_unseen = True
                w2 = prev_word2 + " " + word
                if w2 in d:
                    p2 = d[w2]
                else:
                    bigram_unseen = True
                w1 = word
                if w1 in d:
                    p1 = d[w1]
                else:
                    unigram_unseen = True
                if not trigram_unseen:
                    pi = np.log10(l3*p3 + l2*p2 + l1*p1)
                    pi = round(pi,10)
                    output.write(str(order) +": lg P(" + word +" | "+ prev_word1 + " " + prev_word2 + ") = " + str(pi)+"\n" )
                    lgprob =lgprob + pi
                elif not bigram_unseen:
                    pi = np.log10(l2*p2 +l1*p1)
                    pi = round(pi,10)
                    output.write(str(order) +": lg P(" + word +" | "+ prev_word1 + " " + prev_word2 + ") = " + str(pi) + " (unseen ngrams)\n" )
                    lgprob =lgprob + pi
                elif not unigram_unseen:
                    pi = np.log10(l1*p1)
                    pi = round(pi,10)
                    output.write(str(order) +": lg P(" + word +" | "+ prev_word1 + " " + prev_word2 + ") = " + str(pi) + " (unseen ngrams)\n" )
                    lgprob =lgprob + pi
                else:
                    output.write(str(order) +": lg P(" + word +" | "+ prev_word1 + " " + prev_word2 + ") = " + "-inf (unknown word)\n" )
                    oov = oov + 1
                prev_word1 = prev_word2
                prev_word2 = word
                continue
            if len(prev_word1) != 0 and len(prev_word2) == 0:
                bigram_unseen = False
                unigram_unseen = False
                prev_word2 = word
                w2 = prev_word1 + " " + prev_word2
                w1 = prev_word2
                if w2 in d:
                    p2 = d[w2]
                else:
                    bigram_unseen = True
                if w1 in d:
                    p1 = d[w1]
                else:
                    unigram_unseen = True
                if not bigram_unseen:
                    pi = np.log10(l1*p1 + l2*p2)
                    pi = round(pi,10)
                    output.write(str(order) +": lg P(" + word +" | "+ prev_word1 + ") = " + str(pi) + "\n"  )
                    lgprob =lgprob + pi
                elif not unigram_unseen:
                    pi = np.log10(l1*p1)
                    pi = round(pi,10)
                    output.write(str(order) +": lg P(" + word +" | "+ prev_word1 + ") = " + str(pi) + " (unseen ngrams)\n" )
                    lgprob =lgprob + pi
                else:
                    output.write(str(order) +": lg P(" + word +" | "+ prev_word1 +  ") = "  + "-inf (unknown word)\n" )
                    oov = oov + 1
                continue
            if len(prev_word1) == 0 and len(prev_word2) == 0:
                prev_word1 = word
                continue
        output.write('1 sentence, ' + str(order - 1) + ' words, '+ str(oov) + ' OOVs\n')
        output.write('lgprob=' + str(round(lgprob,10)) + ' ppl=' + str(round(np.power(10,-lgprob/(order-oov)),10)) +'\n\n\n\n')
        oov_total = oov_total + oov
        word_total = word_total + order - 1
        lg_total = lg_total + lgprob
    output.write('\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n')
    cnt = word_total + sn - oov_total
    avg = float(lg_total/cnt)
    avg = round(avg,10)
    ppl_total = np.power(10,-avg)
    ppl_total = round(ppl_total,10)
    output.write('sent_num='+ str(sn) + ' word_num=' + str(word_total) + ' oov_num='+ str(oov_total)+'\n')
    output.write('lgprob=' + str(lg_total) + ' ave_lgprob='+str(avg) + ' ppl=' +str(ppl_total))
