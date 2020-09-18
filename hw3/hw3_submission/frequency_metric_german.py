import re
import sys
import math
'''read europarl-v7.de-en.true.de and count the frequency of each word'''
d = dict()
with open('./europarl-v7.de-en.true.de', 'r') as f:
    for line in f:
        words = line.split(" ")
        for word in words:
            word = word.lower()
            if word in d:
                d[word] = d[word] + 1
            else:
                d[word] = 1

for line in sys.stdin:
    frequency = []
    print_d = dict()
    word = line.strip("\n")
    word = word.lower()
    "no spliting"
    if word in d.keys():
        freq = d[word]
    else:
        freq = 0
        "split the word to two sub words"
    if freq != 0:
        frequency.append(freq)
        print_d[freq] = word + " = " + word + " (" + str(freq) + ") " + "= " + str(freq)
    for i in range(1,len(word)):
        sub1 = word[:i]
        sub2 = word[i:]
        if sub1 in d.keys():
            freq1 = d[sub1]
        else:
            freq1 = 0
        if sub2 in d.keys():
            freq2 = d[sub2]
        else:
            freq2 = 0
        freq = math.sqrt((freq1)*(freq2))
        if freq != 0:
            frequency.append(freq)
            print_d[freq] = sub1 + " " + sub2 + " = " + sub1 + " (" + str(freq1) + ") " + sub2 + " (" + str(freq2) + ") " + "= " + str(freq)
    for i in range(1,len(word)-1):
        for j in range(i + 1,len(word)):
            has_connector = False
            sub1 = word[:i]
            sub2 = word[i:j]
            sub3 = word[j:]
            freq_sub = []
            for sub in [sub1,sub2,sub3]:
                if sub in d.keys():
                    freq_sub.append(d[sub])
                else:
                    freq_sub.append(0)
                i = i + 1
            if sub2 in ['n','en','s','es']:
                has_connector = True
            if has_connector == False:
                freq = ((freq_sub[0])*(freq_sub[1])*(freq_sub[2]))**(float(1)/3)
                if freq != 0:
                    frequency.append(freq)
                    print_d[freq] = sub1 + " " + sub2 + " " + sub3 + " = " + sub1 + " (" + str(freq_sub[0]) + ") " + sub2 + " (" + str(freq_sub[1]) + ") " + sub3 + " (" + str(freq_sub[2]) + ") " + "= " + str(freq)
            else:
                freq = math.sqrt((freq_sub[0])*(freq_sub[2]))
                if freq != 0:
                    frequency.append(freq)
                    print_d[freq] = sub1 + " "  + sub3 + " = " + sub1 + " (" + str(freq_sub[0]) + ") "  + sub3 + " (" + str(freq_sub[2]) + ") " + "= " + str(freq)

    for i in range(1,len(word)-2):
        for j in range(i + 1,len(word)-1):
            for k in range(j + 1, len(word)):
                has_connector2 = False
                has_connector3 = False
                sub1 = word[:i]
                sub2 = word[i:j]
                sub3 = word[j:k]
                sub4 = word[k:]
                freq_sub=[]
                #print(word)
                for sub in [sub1,sub2,sub3,sub4]:
                    #print(sub)
                    if sub in d.keys():
                        freq_sub.append(d[sub])
                    else:
                        freq_sub.append(0)
                if sub2 in ['n','en','s','es']:
                    has_connector2 = True
                if sub3 in ['n','en','s','es']:
                    has_connector3 = True
                if has_connector2:
                    freq = ((freq_sub[0])*(freq_sub[2])*(freq_sub[3]))**(float(1)/3)
                    if freq != 0:
                        frequency.append(freq)
                        print_d[freq] = sub1 + " " + sub3 + " " + sub4 + " = " + sub1 + " (" + str(freq_sub[0]) + ") " + sub3 + " (" + str(freq_sub[2]) + ") " + sub4 + " (" + str(freq_sub[3]) + ") " + "= " + str(freq)
                if has_connector3:
                    freq = ((freq_sub[0])*(freq_sub[1])*(freq_sub[3]))**(float(1)/3)
                    if freq != 0:
                        frequency.append(freq)
                        print_d[freq] = sub1 + " " + sub2 + " " + sub4 + " = " + sub1 + " (" + str(freq_sub[0]) + ") " + sub2 + " (" + str(freq_sub[1]) + ") " + sub4 + " (" + str(freq_sub[3]) + ") " + "= " + str(freq)
                        #print("H")
                        #print(type(frequency))
    frequency.sort(reverse = True)
    #print (frequency)
    for freq in frequency:
        print(print_d[freq])
