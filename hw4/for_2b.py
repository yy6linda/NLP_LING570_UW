import re
import sys


english_line = ''
line_number = 0
d = dict()
for line in sys.stdin:
    pattern = re.compile(r'^#')
    if pattern.search(line):
        line_number = 2
        #print("no.1")
        continue
    if line_number == 2:
        english_line = line.split()
        '''
        print("english_line")
        print(english_line)
        '''
        line_number = line_number + 1
        #print("no.2")
        #print(english_line)
        continue
    if line_number == 3:
        pattern_word = re.compile(r"([a-zA-ZäöüÄÖÜß]+\s\(\{\s[0-9]+\s([0-9]+\s)*\}\))")
        target = re.findall(pattern_word,line)[1:]
        ## erkläre ({ 2 10 }) this is an item
        for item in target:
            #print("This is a new item")
            #print(item)
            empty_list = []
            translation_return = "NULL"
            german_word = re.findall(r'[a-zA-ZäöüÄÖÜß][a-zäöüÄÖÜß]*', item[0])[0]
            #print(german_word)
            number = re.findall(r'\d+', item[0])
            #print(number)
            count = 0
            number_before = 0
            for i in number:
                count = count + 1
                if count == 1:
                    '''
                    print("int(i)")
                    print(int(i))
                    '''
                    translation_return = english_line[int(i)-1]
                    number_before = int(i)
                    #print(number_before)
                if count <= len(number) & count != 1:
                    translation = english_line[int(i)-1]
                    if int(i) == number_before + 1:
                        translation_return = translation_return + " " + translation
                        number_before = int(i)
                    else:
                        translation_return = translation_return + " ... " + translation
                        number_before = int(i)
            if german_word in d:
                '''
                print("location1")
                print(german_word)
                print("type(d[german_word])")
                print(type(d[german_word]))
                '''
                d[german_word].append(translation_return)
                '''
                print(type(d[german_word]))
                print(d[german_word])
                '''
            else:
                empty_list.append(translation_return)
                d[german_word] = empty_list
                '''
                print("location3")
                print(d[german_word])
                '''
        line_number = 0

for key,val in d.items():
    output = key + " "
    d2 = dict()
    for word in val:
        if word in d2:
            d2[word] = d2[word] + 1
        else:
            d2[word] = 1
    sum = 0
    for key, value in d2.items():
        sum = sum + value
        #print(sum)
    remove = []
    for key,value in d2.items():
        d2[key] = d2[key]/sum
        #print(d2[key])
        if d2[key] < 0.01:
            remove.append(key)
    for key in remove:
         del d2[key]
    for key,value in sorted(d2.items(), key=lambda item: item[1],reverse = True):
        output = output + key 
        break
    print(output)
