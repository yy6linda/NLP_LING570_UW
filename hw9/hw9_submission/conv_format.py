import re
import sys
from sys import argv
import string
import operator
import numpy as np

for line in sys.stdin:
    line = line.strip('\n')
    sub = line.split(" => ")
    word_line = sub[0]
    pos_line = sub[1]
    words = word_line.split(" ")
    pos = pos_line.split(" ")[1:-1]
    new_pos = []
    for pos_tag in pos:
        states = pos_tag.split('_')
        to_state = states[1]
        new_pos.append(to_state)
    l_word_pos = []
    converted_line = ''
    for i in range(len(new_pos)):
        l_word_pos.append(words[i]+ '/' + new_pos[i])
    for word_pos in l_word_pos:
        converted_line =  converted_line + word_pos + ' '
    print(converted_line)
