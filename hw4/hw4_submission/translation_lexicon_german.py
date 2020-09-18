import re
import sys
import math
'''read europarl-v7.de-en.true.de and count the frequency of each word'''
'''
create a dictionary for each german  word
der the
sys.argv[1] is for_2b

'''
d = dict()
filename = sys.argv[1]
with open(filename, 'r') as f:
    for line in f:
        line = line.strip('\n')
        de = line.split(' ', 1)[0]
        en = line.split(' ', 1)[1]
        d[de] = en

for line in sys.stdin:
    print_d = dict()
    word = line.strip("\n")
    word = word.lower()
    "no spliting"
    if word in d.keys():
        trans = d[word]
        print(word + " = " + word + " (" + trans + ") ")
    for i in range(1,len(word)-1):
        sub1 = word[:i]
        sub2 = word[i:]
        has_trans1 = False
        has_trans2 = False
        if sub1 in d.keys():
            trans1 = d[sub1]
            has_trans1 = True
        if sub2 in d.keys():
            trans2 = d[sub2]
            has_trans2 = True
        if has_trans1 & has_trans2:
            print(sub1 + " " + sub2 + " = " + sub1 + " (" + trans1 + ") " + sub2 + " (" + trans2 + ") " )
    for i in range(1,len(word)-2):
        for j in range(i + 2,len(word)-1):
            has_connector = False
            sub1 = word[:i]
            sub2 = word[i:j]
            sub3 = word[j:]
            has_trans1 = False
            has_trans2 = False
            has_trans3 = False
            if sub1 in d.keys():
                trans1 = d[sub1]
                has_trans1 = True
            if sub2 in d.keys():
                trans2 = d[sub2]
                has_trans2 = True
            if sub3 in d.keys():
                trans3 = d[sub3]
                has_trans3 = True
            if (sub2 in ['n','en','s','es'])& has_trans1 & has_trans3:
                print(sub1 + " " + sub3 + " = " + sub1 + " (" + trans1 + ") " + sub3 + " (" + trans3 + ") " )
            if has_trans1 & has_trans2 & has_trans3 & (sub2 not in ['n','en','s','es']):
                print( sub1 + " " + sub2 + " " + sub3 + " = " + sub1 + " (" + trans1 + ") " + sub2 + " (" + trans2 + ") " + sub3 + " (" + trans3 + ") ")

    for i in range(1,len(word)-3):
        for j in range(i + 2,len(word)-2):
            for k in range(j + 2, len(word)-1):
                sub1 = word[:i]
                sub2 = word[i:j]
                sub3 = word[j:k]
                sub4 = word[k:]
                has_trans1 = False
                has_trans2 = False
                has_trans3 = False
                has_trans4 = False
                if sub1 in d.keys():
                    trans1 = d[sub1]
                    has_trans1 = True
                if sub2 in d.keys():
                    trans2 = d[sub2]
                    has_trans2 = True
                if sub3 in d.keys():
                    trans3 = d[sub3]
                    has_trans3 = True
                if sub4 in d.keys():
                    trans4 = d[sub4]
                    has_trans4 = True
                if (sub2 in ['n','en','s','es'])& has_trans1 & has_trans3 & has_trans4:
                    print(sub1 + " " + sub3 + " " + sub4 + " = " + sub1 + " (" + trans1 + ") " + sub3 + " (" + trans3 + ") " + sub4 + " (" + trans4 + ") ")
                if (sub3 in ['n','en','s','es'])& has_trans1 & has_trans2 & has_trans4:
                    print(sub1 + " " + sub2 + " " + sub3 + " = " + sub1 + " (" + trans1 + ") " + sub2 + " (" + trans2 + ") " + sub4 + " (" + trans4 + ") ")
