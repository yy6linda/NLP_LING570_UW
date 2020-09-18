import re
import sys



pattern = re.compile(r'\(SIGMA\s\w\)')
for line in sys.stdin:
    line = line.strip('\n')
    target = re.findall(pattern,line)
    converted_line = ""
    for i in range(0,len(target)):
        converted_line = converted_line + target[i][7] + " "
    print(converted_line)
    
'''
if __name__ == "__main__":
    pattern = re.compile(r'\(SIGMA\s\w\)')
    s = '(ROOT (WORD (WORD (SIGMA f) (SIGMA a) (SIGMA i) (SIGMA t) (SIGMA h)) (SUFFIX (SIGMA l) (SIGMA e) (SIGMA s) (SIGMA s)))\n(ROOT (WORD (WORD (SIGMA f) (SIGMA a) (SIGMA i) (SIGMA t) (SIGMA h)) (SUFFIX (SIGMA l) (SIGMA e) (SIGMA s) (SIGMA s)))'
    print(s)
    for line in s:
        line = line.strip('\n')
        target = re.findall(pattern,line)
        converted_line = ""
        for i in range(0,len(target)):
            converted_line = converted_line + target[i][7] + " "
        print(converted_line)
    target = re.findall(pattern,s)

    converted_line = ""
    for i in range(0,len(target)):
        converted_line = converted_line + target[i][7] + " "

    print(converted_line)
    '''
