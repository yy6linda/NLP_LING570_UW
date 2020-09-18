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
    output_line = ""
    line = line.strip("\n")
    words = line.split(" ")
    for word in words:
        word = word.lower()
        frequency = []
        print_d = dict()
        "no spliting"
        if word in d.keys():
            freq = d[word]
            frequency.append(freq)
            print_d[freq] =  word
        for i in range(1,len(word)-1):
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
                print_d[freq] = sub1 + " " + sub2
        for i in range(1,len(word)-2):
            for j in range(i + 2,len(word)-1):
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
                if sub2 in ['n','en','s','es']:
                    has_connector = True
                if has_connector == False:
                    freq = ((freq_sub[0])*(freq_sub[1])*(freq_sub[2]))**(float(1)/3)
                    if freq != 0:
                        frequency.append(freq)
                        print_d[freq] = sub1 + " " + sub2 + " " + sub3
                else:
                    freq = math.sqrt((freq_sub[0])*(freq_sub[2]))
                    if freq != 0:
                        frequency.append(freq)
                        print_d[freq] = sub1 + " "  + sub3
        for i in range(1,len(word)-3):
            for j in range(i + 2,len(word)-2):
                for k in range(j + 2, len(word)-1):
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
                            print_d[freq] = sub1 + " " + sub3 + " " + sub4
                    if has_connector3:
                        freq = ((freq_sub[0])*(freq_sub[1])*(freq_sub[3]))**(float(1)/3)
                        if freq != 0:
                            frequency.append(freq)
                            print_d[freq] = sub1 + " " + sub2 + " " + sub4
        frequency.sort(reverse = True)
        #print(print_d)
        #print(frequency)
        if len(frequency) == 0:
            word_freq = word
        else:
            freq_highest = frequency[0]
            word_freq = print_d[freq_highest]
        output_line = output_line + word_freq + " "
    print(output_line)
