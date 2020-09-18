import re
import sys
from sys import argv
import string
import numpy as np
'''convert input and gold to "tooo" type, where "t" stands for the start of a token,
"o" for inside of a token, white space is not counted'''

d_uni = dict()
d_bi = dict()
d_tri = dict()

uni_token = 0
bi_token = 0
tri_token = 0
with open(sys.argv[1], 'r') as f:
    for line in f:
        words = line.split("\t")
        if len(words[1].split()) == 1:
            uni_token = uni_token + int(words[0])
            #print(words[1].strip("\n"))
            d_uni[words[1].strip("\n")] = int(words[0])
        if len(words[1].split()) == 2:
            #print(words[1].strip("\n"))
            bi_token = bi_token + int(words[0])
            d_bi[words[1].strip("\n")] = int(words[0])
        if len(words[1].split()) == 3:
            tri_token = tri_token + int(words[0])
            d_tri[words[1].strip("\n")] = int(words[0])

sorted_d_uni = sorted(d_uni.items(), key=lambda x:  (-1*x[1],  x[0]), reverse=False)
sorted_d_bi = sorted(d_bi.items(), key=lambda x: (-1*x[1],  x[0]), reverse=False)
sorted_d_tri = sorted(d_tri.items(), key=lambda x:  (-1*x[1],  x[0]), reverse=False)

# uni[0] Pierre /// uni[1] 2
output = open(sys.argv[2], 'w')
output.write('\\data\\\n')
output.write('ngram 1: type=' + str(len(d_uni)) + ' token='+ str(uni_token) +'\n')
output.write('ngram 2: type=' + str(len(d_bi)) + ' token='+ str(bi_token) +'\n')
output.write('ngram 3: type=' + str(len(d_tri)) + ' token='+ str(tri_token) +'\n')
output.write('\n')
output.write('\\1-grams:\n')
for uni in sorted_d_uni:
    prob = float(uni[1]/uni_token)
    prob = round(prob, 10)
    lg_prob = np.log10(prob)
    lg_prob = round(lg_prob,10)
    output.write(str(uni[1])+ ' '+ str(prob) + ' ' + str(lg_prob) + ' ' + uni[0]+'\n')
output.write('\n')
output.write('\\2-grams:\n')
for bi in sorted_d_bi:
    prob = float(bi[1]/d_uni[bi[0].split(" ")[0]])
    prob = round(prob, 10)
    lg_prob = np.log10(prob)
    lg_prob = round(lg_prob,10)
    output.write(str(bi[1])+ ' ' + str(prob) + ' ' + str(lg_prob) + ' ' + bi[0]+'\n')
output.write('\n')
output.write('\\3-grams:\n')
for tri in sorted_d_tri:
    prob = float(tri[1]/d_bi[' '.join(tri[0].split(" ")[:2])])
    prob = round(prob, 10)
    lg_prob = np.log10(prob)
    lg_prob = round(lg_prob,10)
    output.write(str(tri[1])+ ' '+ str(prob) + ' ' + str(lg_prob) + ' ' + tri[0]+'\n')
