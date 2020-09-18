import re
import sys

def convert(pattern):
    pattern = pattern.replace(" ", "")
    separator_index = pattern.find(":")
    word1 = pattern[1:separator_index]
    #print(word1)
    word2 = pattern[(separator_index + 1):-1]
    #print(word2)
    if word2 =='stem':
        word2 = "word"
    word2 = word2.upper()
    converted_word1 = ""
    for i in word1:
        #print(i)
        converted_word1 =   converted_word1 +" (SIGMA " + i + ")"
    return  "(" + word2+ converted_word1 + ")"

pattern = re.compile(r'\(\s?[a-z]+\s?:\s?[a-z]+\s?\)')

for line in sys.stdin:
    line = line.strip('\n')
    line = line.split(' ', 1)[1]
    line = line.replace('S','WORD')
    target = re.findall(pattern,line)
    for i in range(0,len(target)):
        line = line.replace(target[i],convert(target[i]))
    print("(ROOT " + line + ")")
'''
if __name__ == "__main__":
    pattern = re.compile(r'[a-z]+\s?:\s?[a-z]+')
    s = "cyclically (S (S (S (cycle :stem) (ic: suffix)) (al : suffix)) (ly:suffix))"
    s = s.split(' ', 1)[1]
    s = s.replace('S','WORD')
    target = re.findall(pattern,s)
    print(target)
    for i in range(0,len(target)):
        s = s.replace(target[i],convert(target[i]))
    s = "(ROOT " + s + ")"
    print(s)
'''
