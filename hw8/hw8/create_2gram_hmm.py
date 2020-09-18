import re
import sys
from sys import argv
import string
import operator
import numpy as np

d_init = dict()
d_trans = dict()
d_emiss= dict()
d_state = dict()
d_symbol = dict()

'''
d_init = [BOS]
d_trans =[(BOS,DT),(DT,N)...]
d_emiss =[(DT,the),(DT,a)]
line = Pierre/NNP Vinken/NNP ,/, 61/CD years/NNS old/JJ ,/, will/MD join/VB the/DT board/NN as/IN a/DT nonexecutive/JJ director/NN Nov./NNP 29/CD ./.

'''
state_num = 0
sym_num = 0
init_line_num = 1
trans_line_num = 0
emiss_line_num = 0
'''sys.stdin will read the training data'''
'''A special situation Macmillan\/McGraw-Hill/NNP'''
def bos_eos(line):
    line = 'bos/BOS ' + line + ' eos/EOS'
    return line
for line in sys.stdin:
    line = line.strip('\n')
    line = bos_eos(line)
    words = line.split(" ")
    prev = ""
    for words in words:
        word = words.split("/")
        if "\/" in words:
             #print(word)
             new_word= ''.join(word[:2])
             new_state= word[2]
             word[0] = new_word
             word[1] = new_state
        if word[1] in d_state:
            d_state[word[1]] = d_state[word[1]] + 1
        else:
            d_state[word[1]] = 1
        if word[0] in d_symbol:
            d_symbol[word[0]] = d_symbol[word[0]] + 1
        else:
            d_symbol[word[0]] = 1
        emiss = (word[1],word[0])
        if emiss in d_emiss:
            d_emiss[emiss] = d_emiss[emiss] + 1
        else:
            d_emiss[emiss] = 1
        if len(prev) != 0:
            trans = (prev,word[1])
            if trans in d_trans:
                d_trans[trans] = d_trans[trans] + 1
            else:
                d_trans[trans] = 1
        prev = word[1]
state_num = len(d_state)
sym_num = len(d_symbol)
init_line_num = 1
trans_line_num =len(d_trans)
emiss_line_num = len(d_emiss)
'''sorted dictionary'''
sorted_d_trans = sorted(d_trans.items(), key=lambda x:  (x[0]), reverse=False)
sorted_d_emiss = sorted(d_emiss.items(), key=lambda x:  (x[0]), reverse=False)
output = open(sys.argv[1], 'w')
output.write('state_num=' + str(state_num)+'\n')
output.write('sym_num=' + str(sym_num)+'\n')
output.write('init_line_num=' + str(init_line_num) + '\n')
output.write('trans_line_num=' + str(trans_line_num) + '\n')
output.write('emiss_line_num=' + str(emiss_line_num) + '\n')
output.write('\n\\init\n')
output.write('BOS\t1.0\t0.0\n\n\n')
output.write('\\transition\n')
for trans in sorted_d_trans:
    prob = round(float(trans[1]/d_state[trans[0][0]]),10)
    lgprob = round(np.log10(prob),10)
    output.write(trans[0][0]+'\t'+trans[0][1]+ '\t'+str(prob) +'\t'+str(lgprob)+ '\n')
output.write('\n\n\\emission\n')
for emiss in sorted_d_emiss:
    prob = round(float(emiss[1]/d_state[emiss[0][0]]),10)
    lgprob = round(np.log10(prob),10)
    output.write(emiss[0][0]+'\t'+emiss[0][1]+ '\t'+str(prob) +'\t'+str(lgprob)+ '\n')
