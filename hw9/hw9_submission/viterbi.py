import re
import sys
from sys import argv
import string
import operator
import numpy as np


d_init = dict()
d_trans = dict()
d_emiss = dict()
l_symbol = []
l_state = []
l_word = []
input_hmm = sys.argv[1]
test_file = sys.argv[2]
output_file = sys.argv[3]
output = open(output_file, 'w')
stderr = open('stderr', 'w')

with open(input_hmm, 'r') as f:
    initial_checker = False
    transition_checker = False
    emission_checker = False
    init_line_num = 0
    trans_line_num = 0
    emiss_line_num = 0
    prev_state_trans = ''
    prev_state_emiss = ''
    for line in f:
        line = line.strip('\n')
        line = line.strip('')
        if len(line) == 0:
            continue
        if transition_checker and 'emission' not in line:
            words = line.split()
            words = [x for x in words if len(x) != 0]
            trans = (words[0], words[1])
            prob = float(words[2])
            if prob < 0 or prob > 1:
                stderr.write(
                    "warning: the prob is not in [0,1] range:  " + line)
            else:
                if trans not in d_trans:
                    d_trans[trans] = prob

        if emission_checker:
            words = line.split()
            words = line.split()
            words = [x for x in words if len(x) != 0]
            emiss = (words[0], words[1])
            if words[1] not in l_word:
                l_word.append(words[1])
            prob = float(words[2])
            if prob < 0 or prob > 1:
                stderr.write("warning: the prob is not in [0,1] range:  " + line)
            else:
                if emiss not in d_emiss:
                    d_emiss[emiss] = prob

        if '\\transition' in line:
            initial_checker = False
            transition_checker = True
        if '\\emission' in line:
            transition_checker = False
            emission_checker = True
'''information from hmm loaded'''

with open(test_file, 'r') as f:
    for line in f:
        line = line.strip('\n')
        line = line.strip('')
        words = line.split()
        line_tag = ''
        count = 1
        l_from_state = []
        l_from_state_prob = []
        path = []
        max_path = ''
        max_prob = 0
        for word in words:
            if word not in l_word:
                word = '<unk>'
            l_to_state = []
            l_to_state_prob = []
            l_v_prob = []
            '''for the first word'''
            tag = ''
            if count == 1:
                d_word = dict()
                d_word = {k: v for k, v in d_emiss.items() if k[1] == word}
                for item in d_word:
                    l_to_state.append(item[0])
                    l_to_state_prob.append(d_word[item])
                    trans = ('BOS_BOS', item[0])
                    if trans in d_trans:
                        trans_prob = d_trans[trans]
                    else:
                        trans_prob = 0
                    v_prob = trans_prob * d_emiss[item]
                    l_v_prob.append(v_prob)
                max_index = l_v_prob.index(max(l_v_prob))
                tag = l_to_state[max_index]
                non_zero_index = [i for i, e in enumerate(l_v_prob) if e != 0]
                l_to_state = list(l_to_state[i] for i in non_zero_index)
                l_v_prob = list(l_v_prob[i] for i in non_zero_index)
                for state in l_to_state:
                    path.append('BOS_BOS' + ' ' + state)
                l_from_state = l_to_state
                l_from_state_prob = l_v_prob
            else:
                '''maximum value of pre viterbi probability and transition probability'''
                # print(word)
                d_word = dict()
                d_word = {k: v for k, v in d_emiss.items() if k[1] == word}
                for item in d_word:
                    max_va = 0
                    pre_state = ''
                    l_to_state.append(item[0])
                    to_state = item[0]
                    l_to_state_prob.append(d_word[item])
                    for c, i in enumerate(l_from_state):
                        trans = (i, to_state)
                        if trans in d_trans:
                            trans_prob = d_trans[trans]
                        else:
                            trans_prob = 0
                        va = l_from_state_prob[c] * trans_prob
                        if va > max_va:
                            max_va = va
                            pre_state = i
                    for n, i in enumerate(path):
                        if len(pre_state) > 0 and i.endswith(pre_state) and len(i.split()) == count:
                            path.append(path[n] + ' ' + to_state)
                            break
                    l_v_prob.append(max_va * d_word[item])
                non_zero_index = [i for i, e in enumerate(l_v_prob) if e != 0]
                l_to_state = list(l_to_state[i] for i in non_zero_index)
                l_v_prob = list(l_v_prob[i] for i in non_zero_index)
                l_from_state = l_to_state
                l_from_state_prob = l_v_prob
            l_rm = []
            for p in path:
                s = p.split()
                if len(s) != count + 1:
                    l_rm.append(p)
            for item in l_rm:
                path.remove(item)
            count = count + 1
            if count == len(words) + 1:
                max_index = l_from_state_prob.index(max(l_from_state_prob))
                max_prob = max(l_from_state_prob)
                max_prob = np.log10(max_prob)
                tag = l_from_state[max_index]
                for p in path:
                    if p.endswith(tag):
                        max_path = p
        output.write(line)
        output.write(' => ')
        output.write(max_path + ' ')
        output.write(str(max_prob))
        output.write('\n')
