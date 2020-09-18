import re
import sys
from sys import argv
import string
import operator
import numpy as np
'''convert input and gold to "tooo" type, where "t" stands for the start of a token,
"o" for inside of a token, white space is not counted'''

d_init = dict()
d_trans = dict()
d_emiss= dict()
l_symbol = []
l_state = []
input_hmm = sys.argv[1]
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
        if 'state_num' in line:
            format = re.compile("[0-9]+")
            old_state_num = int(re.findall(format,line)[0])
        if 'sym_num' in line:
            format = re.compile("[0-9]+")
            old_sym_num = int(re.findall(format,line)[0])
        if 'init_line_num' in line:
            format = re.compile("[0-9]+")
            old_init_line_num = int(re.findall(format,line)[0])
        if 'trans_line_num' in line:
            format = re.compile("[0-9]+")
            old_trans_line_num = int(re.findall(format,line)[0])
        if 'emiss_line_num' in line:
            format = re.compile("[0-9]+")
            old_emiss_line_num = int(re.findall(format,line)[0])

        if initial_checker and 'transition' not in line:
            words = line.split()
            words = [x for x in words if len(x) != 0]
            if len(words) == 3:
                init_line_num = init_line_num + 1


        if transition_checker and 'emission' not in line:
            words = line.split()
            #print(words)
            words = [x for x in words if len(x) != 0]
            if words[0] in d_trans:
                d_trans[words[0]] = float(d_trans[words[0]]) + float(words[-2])
            else:
                d_trans[words[0]] = float(words[-2])
            if words[0] not in l_state:
                l_state.append(words[0])
            if words[1] not in l_state:
                l_state.append(words[1])
            trans_line_num = trans_line_num + 1

        if emission_checker:
            words = line.split()
            words = [x for x in words if len(x) != 0]
            if words[0] in d_emiss:
                d_emiss[words[0]] = d_emiss[words[0]] + float(words[-2])
            else:
                d_emiss[words[0]] = float(words[-2])
            if words[1] not in l_symbol and len(words[1])!=0:
                l_symbol.append(words[1])
            emiss_line_num = emiss_line_num + 1

        if '\\init' in line:
            initial_checker = True
        if '\\transition' in line:
            initial_checker = False
            transition_checker = True
        if '\\emission' in line:
            transition_checker = False
            emission_checker = True

    if old_state_num == len(l_state):
        print("state_num={}".format(old_state_num) )
    else:
        print('warning: different numbers of state_num: claimed={}, real={}'.format(old_state_num, len(l_state)))
    if old_sym_num == len(l_symbol):
        print("sym_num={}".format(old_sym_num))
    else:
        print('warning: different numbers of sym_num: claimed={}, real={}'.format(old_sym_num, len(l_symbol)))
    if old_init_line_num == init_line_num:
        print("init_line_num={}".format(init_line_num))
    else:
        print('warning: different numbers of init_line_num: claimed={}, real={}'.format(old_init_line_num, init_line_num))
    if old_trans_line_num == trans_line_num:
        print("trans_line_num={}".format(trans_line_num))
    else:
        print('warning: different numbers of trans_line_num: claimed={}, real={}'.format(old_trans_line_num, trans_line_num))
    if old_emiss_line_num == emiss_line_num:
        print("emission_line_num={}".format(emiss_line_num))
    else:
        print('warning: different numbers of emission_line_num: claimed={}, real={}'.format(old_emiss_line_num, emiss_line_num))

    for trans in d_trans:
        if  abs(float(d_trans[trans]) - 1) > 0.001:
            print('warning: the trans_prob_sum for state '+trans + ' is ' + str(round(d_trans[trans],10)))
    for state in l_state:
        if state not in d_trans:
            print('warning: the trans_prob_sum for state '+ state + ' is 0' )

    for state in l_state:
        if state not in d_emiss:
            print('warning: the emiss_prob_sum for state '+ state + ' is 0' )
        else:
            if  abs(float(d_emiss[state]) - 1) > 0.001:
                print('warning: the emiss_prob_sum for state '+ state + ' is ' + str(round(d_emiss[state],10)))
        #print(words)
