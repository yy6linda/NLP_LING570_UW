import re
import sys
from sys import argv
import string
import os

d = dict()
train_text = open(sys.argv[1], 'w')
test_text = open(sys.argv[2], 'w')
ratio = float(sys.argv[3])

for args in sys.argv[4:]:
    #print([name for name in os.listdir(args)])
    num = len([name for name in os.listdir(args)])
    #print(num)
    train_num = round(num * ratio)
    #print(train_num)
    tag = args.split("/")[-1]
    count = 0
    for filename in sorted(os.listdir(args)):
        count = count + 1
        with open("temp",'w') as output:
            os.system("python3 proc_file_2.py "+args+"/"+str(filename)+" "+str(tag)+" "+"temp")
        with open("temp",'r') as f:
            for line in f:
                #print(line)
                if count <= train_num:
                    train_text.write(args+ "/" + filename + " " + tag + " " + line + '\n')
                else:
                    test_text.write(args+ "/" + filename + " " + tag + " " + line + '\n')
