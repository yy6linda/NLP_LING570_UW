import re
import sys
from sys import argv
import string

def is_num(input):
    format = re.compile("^~?[0-9]{1,3}((,)?[0-9]{3})*(\.[0-9]+)?")
    if re.match(format,input):
        return True

def is_sign(input):
    return word[0] in '$(#{[<'

def is_abbreviation(input):
    filename = sys.argv[1]
    with open(filename, 'r') as f:
        for line in f:
            for word in line.split():
                if word in input:
                    return word
    return ""

def is_quotation_mark(input):
    if "\"" in input:
        return True

def is_apostrophe(input):
    if "\'" in input:
        return True

def is_percentage(input):
    if '%' in input:
        return True

def apostrophe_change(word):
    if is_apostrophe(word):
        word = re.sub('n\'t',' n\'t',word)
        word = re.sub('\'m',' \'m',word)
        word = re.sub('\'s',' \'s',word)
        word = re.sub('\'ve',' \'ve',word)
        word = re.sub('\'ll',' \'ll',word)
        word = re.sub('\'re',' \'re',word)
        return word
    else:
        return word
def is_one_letter(word):
    return len(word) == 1
'''check if there is punctuation at the end of token'''
def check_punctuation_at_end(word, punctuation):
    if word[len(word) - 1] in punctuation:
       punc = " " + word[len(word) - 1]
       word = word[:(len(word) - 1)]
    else:
       punc = ""
    return word, punc

def is_initial(word):
    format = re.compile("[A-Z]((\.[A-Za-z])+(\.)?|\.)")
    if re.match(format,word):
        return True

if __name__ == "__main__":
        for line in sys.stdin:
            punctuation = '#&,.:;<=>?@[\\]^_`{|}~()*!"\''
            if len(line.strip()) == 0 :
                print("\n", end = '')
                continue
            line_output = ""
            for word in line.split():
                ''' add if then do something'''
                if is_sign(word):
                    word, punc = check_punctuation_at_end(word, punctuation)
                    line_output =  line_output + word[0] + " " + word[1:] + punc + " "
                    continue
                if is_percentage(word):
                    word, punc = check_punctuation_at_end(word, punctuation)
                    line_output = line_output + word[:(len(word) - 1)] + " %" + punc + " "
                    continue
                if is_num(word):
                    word, punc = check_punctuation_at_end(word, punctuation)
                    line_output =  line_output + word + punc + " "
                    continue
                if len(is_abbreviation(word)) != 0:
                   if len(is_abbreviation(word)) == len(word):
                      line_output = line_output + word + " "
                   elif word[(len(word)-2):] =="\'s":
                      line_output = line_output + is_abbreviation(word)+ " \'s"
                   else:
                      word, punc = check_punctuation_at_end(word, punctuation)
                      line_output = line_output + word + punc + " "
                   continue
                if is_quotation_mark(word):
                    if word[0] == "\"" and word[len(word) - 1] == "\"" and word[len(word) - 2] in punctuation:
                        line_output = line_output + "`` " + apostrophe_change(word[1:(len(word) - 2)]) + " " + word[len(word) - 2] + " '' "
                    elif word[0] == "\"" and word[len(word) - 1] == "\"":
                        line_output = line_output + "`` " + apostrophe_change(word[1:(len(word) - 1)]) +  " '' "
                    elif word[len(word) - 1] == "\"" and word[len(word) - 2] in punctuation:
                        line_output = line_output + apostrophe_change(word[:(len(word) - 2)]) + " " + word[len(word) - 2] + " '' "
                    elif word[len(word) - 2] == "\"" and word[len(word) - 1] in punctuation:
                        line_output = line_output + apostrophe_change(word[:(len(word) - 2)]) +  " '' " + word[len(word) - 1] + " "
                    elif word[0] == "\"":
                        line_output = line_output + "`` " + apostrophe_change(word[1:]) + " "
                    elif word[len(word) - 1] == "\"":
                        line_output = line_output + apostrophe_change(word[:(len(word) - 1)]) + " '' "
                    continue
                if is_initial(word):
                    line_output = line_output + word + " "
                    continue
                if is_one_letter(word):
                    line_output = line_output + word + " "
                    continue
                if is_apostrophe(word):
                    word, punc = check_punctuation_at_end(word, punctuation)
                    line_output =  line_output + apostrophe_change(word) + punc + " "
                    continue
                output_word = ''
                for letter in word:
                    if letter in punctuation:
                        output_word = output_word + " " + letter
                    else:
                        output_word = output_word + letter
                line_output = line_output + output_word + " "

            print(line_output)
