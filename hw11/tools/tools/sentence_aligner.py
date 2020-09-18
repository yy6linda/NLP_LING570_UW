import re
import sys
from sys import argv
import string
import operator
import numpy as np

l_en = []
l_de = []
with open(sys.argv[1], 'r') as f:
    for line in f:
        line = line.strip("\n")
        if not line.startswith('<'):
            l_de.append(line)
with open(sys.argv[2], 'r') as f:
    for line in f:
        line = line.strip("\n")
        if not line.startswith('<'):
            l_en.append(line)

for i in range(len(l_en)):
    print(l_de[i] + '\t' + l_en[i])
