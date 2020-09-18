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
d_uni = dict()#the same as d_state
d_bi = dict()
d_tri = dict()
d_unk = dict()
d_emiss_unk = dict()
output = open(sys.argv[1], 'w')
l1 = float(sys.argv[2])
l2 = float(sys.argv[3])
l3 = float(sys.argv[4])
unk = sys.argv[5]
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

training = sys.stdin.readlines()
#print(training)
for line in training:
    prev1 = 'BOS'
    prev2 = ''
    line = line.strip('\n')
    line = bos_eos(line)
    words = line.split(" ")
    prev = ""
    #print(line)
    words = [x for x in words if len(x) != 0]
    for words in words:
        word = words.split("/")
        #print(word)
        if "\/" in words:
             #print(word)
             new_word= ''.join(word[:2])
             new_state= word[2]
             word[0] = new_word
             word[1] = new_state
        #count uni_tag
        if word[1] in d_state:
            d_state[word[1]] = d_state[word[1]] + 1
        else:
            d_state[word[1]] = 1
        #count bi_tag
        if len(prev2)!=0:
            bi = prev2 + '_' + word[1]
            #print(bi)
            if bi in d_bi:
                d_bi[bi] = d_bi[bi] + 1
            else:
                d_bi[bi] = 1
        if len(prev2)==0 and len(prev1)!=0:
            bi = prev1 + '_' + word[1]
            if bi in d_bi:
                d_bi[bi] = d_bi[bi] + 1
            else:
                d_bi[bi] = 1
            #print(bi)
        #count tri_tag
        if len(prev1)!=0 and len(prev2)!=0:
            tri = prev1 +'_'+ prev2 + '_' + word[1]
            #print(tri)
            if tri in d_tri:
                d_tri[tri] = d_tri[tri] + 1
            else:
                d_tri[tri] = 1
        if word[0] in d_symbol:
            d_symbol[word[0]] = d_symbol[word[0]] + 1
        else:
            d_symbol[word[0]] = 1
        if len(prev2)!=0:
            emiss = (prev2+'_'+word[1],word[0])
            if emiss in d_emiss:
                d_emiss[emiss] = d_emiss[emiss] + 1
            else:
                d_emiss[emiss] = 1
        if len(prev1) == 0 and len(prev2) == 0:
            emiss = ('BOS_' + word[1],word[0])
            if emiss in d_emiss:
                d_emiss[emiss] = d_emiss[emiss] + 1
            else:
                d_emiss[emiss] = 1
            prev1 = word[1]
            continue
        if len(prev1) != 0 and len(prev2) ==0:
            emiss = (prev1+'_'+word[1],word[0])
            if emiss in d_emiss:
                d_emiss[emiss] = d_emiss[emiss] + 1
            else:
                d_emiss[emiss] = 1
            prev2 = word[1]
            continue
        if len(prev1) != 0 and len(prev2) !=0:
            prev1 = prev2
            prev2 = word[1]

tag_total = 0
for state in d_state:
    tag_total = tag_total + d_state[state]

with open(unk, 'r') as f:
    for line in f:
        line = line.strip('\n')
        words = line.split(' ')
        d_unk[words[0]] = round(float(words[1]),10)
    for pair in d_bi:
        state = pair.split('_')
        to_state = state[1]
        if to_state in d_unk:
            emiss = (pair,'<unk>')
            d_emiss_unk[emiss] = d_unk[state[1]]

for pair in d_emiss:
    state = pair[0].split('_')
    to_state = state[1]
    if to_state in d_unk:
        p_unk = float(d_unk[to_state])
    else:
        p_unk = 0
    d_emiss[pair] = round(float(d_emiss[pair]/d_state[to_state]) * (1-p_unk),10)

for unk in d_emiss_unk:
    d_emiss[unk] = d_emiss_unk[unk]

for line in training:
    prev1 = 'BOS'
    prev2 = ''
    line = line.strip('\n')
    line = bos_eos(line)
    words = line.split(" ")
    words = [x for x in words if len(x) != 0]
    for words in words:
        word = words.split("/")
        if "\/" in words:
             new_word= ''.join(word[:2])
             new_state= word[2]
             word[0] = new_word
             word[1] = new_state
        if len(prev1) != 0 and len(prev2) !=0:
            p_tri = float(d_tri[prev1+'_'+prev2+'_'+word[1]])/float(d_bi[prev1+'_'+prev2])
            p_bi = float(d_bi[prev2+'_'+word[1]])/float(d_state[prev2])
            p_uni = float(d_state[word[1]])/tag_total
            p = round(l3*p_tri + l2*p_bi + l1*p_uni,10)
            trans = (prev1+'_'+prev2, prev2+'_'+word[1])
            if trans not in d_trans:
                d_trans[trans] = p
                #print(p)
    
        if len(prev1) != 0 and len(prev2) ==0:
            prev2 = word[1]
            continue
        if len(prev1) != 0 and len(prev2) !=0:
            prev1 = prev2
            prev2 = word[1]


state_num = len(d_bi)
'''+1 is for <unk>'''
sym_num = len(d_symbol)+1
init_line_num = 1
trans_line_num =len(d_trans)
emiss_line_num = len(d_emiss)

sorted_d_trans = sorted(d_trans.items(), key=lambda x:  (x[0]), reverse=False)
sorted_d_emiss = sorted(d_emiss.items(), key=lambda x:  (x[0]), reverse=False)
output.write('state_num=' + str(state_num)+'\n')
output.write('sym_num=' + str(sym_num)+'\n')
output.write('init_line_num=' + str(init_line_num) + '\n')
output.write('trans_line_num=' + str(trans_line_num) + '\n')
output.write('emiss_line_num=' + str(emiss_line_num) + '\n')
output.write('\n\\init\n')
output.write('BOS\t1.0\t0.0\n\n\n')
sorted_d_trans = sorted(d_trans.items(), key=lambda x:  (x[0]), reverse=False)
sorted_d_emiss = sorted(d_emiss.items(), key=lambda x:  (x[0]), reverse=False)
output.write('\\transition\n')
for trans in sorted_d_trans:
    output.write(trans[0][0]+'\t'+trans[0][1]+'\t'+str(trans[1]) + '\t'+str(round(np.log10(trans[1]),10))+'\n')
output.write('\n\n\\emission\n')
for emiss in sorted_d_emiss:
    output.write(emiss[0][0]+'\t'+emiss[0][1]+'\t'+str(emiss[1])+'\t'+str(round(np.log10(emiss[1]),10))+'\n')
