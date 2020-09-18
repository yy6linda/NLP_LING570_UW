import re
import sys
from sys import argv
import string

d = dict()

input_file = sys.argv[1]
label = sys.argv[2]


output = open(sys.argv[3], 'w')

with open(input_file, 'r') as f:
    checker = False
    for line in f:
        if checker == True:
            line = line.lower()
            line_new = ''
            for letter in line:
                if letter.isalpha():
                    line_new = line_new + letter
                else:
                    line_new = line_new + " "
            words = line_new.split(" ")
            for word in words:
                if word != '':
                    if word in d:
                        d[word] = d[word] + 1
                    else:
                        d[word] = 1
        if line == '\n':
            checker = True

sorted_d = sorted(d.items(), key=lambda x: (x[0]), reverse=False)
output.write(input_file + " " + label + " ")
for item in sorted_d:
    output.write(item[0]+ " " + str(item[1]) + " " )
