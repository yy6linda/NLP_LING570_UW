import re
import sys
from sys import argv
import string
import operator
'''convert input and gold to "tooo" type, where "t" stands for the start of a token,
"o" for inside of a token, white space is not counted'''

d_uni = dict()
d_bi = dict()
d_tri = dict()

def add_eos_bos(line):
    line = line.strip("\n")
    new_line = '<s> '
    new_line = new_line + line
    new_line = new_line.lower()
    new_line = new_line + ' </s>'
    return new_line
'''count unigram'''
with open(sys.argv[1], 'r') as f:
    for line in f:
        line = add_eos_bos(line)
        words = line.split(" ")
        for word in words:
            word = word.lower()
            if word in d_uni:
                d_uni[word] = d_uni[word] + 1
            else:
                d_uni[word] = 1
'''count bigrams'''
with open(sys.argv[1], 'r') as f:
    for line in f:
        line = add_eos_bos(line)
        #print(line)
        words = line.split(" ")
        prev_word = ''
        for word in words:
            word = word.lower()
            if len(prev_word) != 0:
                word_new = prev_word + " " + word
                #print(word_new + " ")
                if word_new in d_bi:
                    d_bi[word_new] = d_bi[word_new] + 1
                else:
                    d_bi[word_new] = 1
            prev_word = word
'''count trigrams'''
with open(sys.argv[1], 'r') as f:
    for line in f:
        line = add_eos_bos(line)
        words = line.split(" ")
        prev_word1 = ''
        prev_word2 = ''
        for word in words:
            word = word.lower()
            if len(prev_word1) != 0 and len(prev_word2) != 0:
                word_new = prev_word1 + " " + prev_word2 + " " + word
                #print(word_new + " ")
                if word_new in d_tri:
                    d_tri[word_new] = d_tri[word_new] + 1
                else:
                    d_tri[word_new] = 1
                prev_word1 = prev_word2
                prev_word2 = word
                continue
            if len(prev_word1) != 0 and len(prev_word2) == 0:
                prev_word2 = word
                continue
            if len(prev_word1) == 0 and len(prev_word2) == 0:
                prev_word1 = word
                continue
output = open(sys.argv[2], 'w')
sorted_d_uni = sorted(d_uni.items(), key=lambda x: (-1*x[1],  x[0]), reverse=False)
sorted_d_bi = sorted(d_bi.items(), key=lambda x: (-1*x[1],  x[0]), reverse=False)
sorted_d_tri = sorted(d_tri.items(), key=lambda x: (-1*x[1],  x[0]), reverse=False)

for uni in sorted_d_uni:
    #print(uni)
    output.write(str(uni[1])+'\t'+uni[0]+'\n')
for bi in sorted_d_bi:
    #print(bi)
    output.write(str(bi[1])+'\t'+bi[0]+'\n')
for tri in sorted_d_tri:
    output.write(str(tri[1])+'\t'+tri[0]+'\n')
