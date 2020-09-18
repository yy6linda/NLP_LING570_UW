import re
import sys
from sys import argv
import string
'''convert input and output to "sooos" type, where "s" stands for boundary,
"o" for inside'''

gold_de = sys.argv[1]
gold_en = sys.argv[2]
raw_de = sys.argv[3]
raw_en = sys.argv[4]
processed_input = ""
with open(raw_de, 'r') as f:
    for line in f:
        count = 0
        for word in line.split():
            if count == 0:
                processed_word = "s"
            else:
                processed_word = "o"
            count = count + 1
            processed_input = processed_input + processed_word
        #print(line)
        #print(processed_input)

processed_gold = ""
with open(gold_de, 'r') as f:
    for line in f:
        count = 0
        for word in line.split():
            if count == 0:
                processed_word = 's'
            else:
                processed_word = 'o'
            count = count + 1
            processed_gold = processed_gold + processed_word

def find(str, ch):
    for i, ltr in enumerate(str):
        if ltr == ch:
            yield i
gold_boundary_index = list(find(processed_gold, "s"))
input_boundary_index = list(find(processed_input, "s"))
def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3
def exclusion(lst1, lst2):
    lst3 = [value for value in lst1 if value not in lst2]
    return lst3
input_gold = intersection(gold_boundary_index,input_boundary_index)
only_input = exclusion(input_boundary_index, input_gold)
only_gold = exclusion(gold_boundary_index, input_gold)
tp = len(input_gold)
fp = len(only_input)
fn = len(only_gold)
'''
print(input_gold)
print(only_input)
print(only_gold)
'''
precision = float(tp)/(tp + fp)
recall = float(tp)/(tp + fn)
f1 = 2 * (float(precision * recall) / (precision + recall))

print("de")
print("precision: " + str(precision))
print("recall: " + str(recall))
print("tp: " + str(tp))
print("fn: " + str(fn))
print("fp: " + str(fp))
print("f1: " + str(f1))

processed_input = ""
with open(raw_en, 'r') as f:
    for line in f:
        count = 0
        for word in line.split():
            if count == 0:
                processed_word = "s"
            else:
                processed_word = "o"
            count = count + 1
            processed_input = processed_input + processed_word
    '''
    print(line)
    print(processed_line)
    print(processed_input)
    '''
processed_gold = ""
with open(gold_en, 'r') as f:
    for line in f:
        count = 0
        for word in line.split():
            if count == 0:
                processed_word = 's'
            else:
                processed_word = 'o'
            count = count + 1
            processed_gold = processed_gold + processed_word

def find(str, ch):
    for i, ltr in enumerate(str):
        if ltr == ch:
            yield i
gold_boundary_index = list(find(processed_gold, "s"))
input_boundary_index = list(find(processed_input, "s"))
def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3
def exclusion(lst1, lst2):
    lst3 = [value for value in lst1 if value not in lst2]
    return lst3
input_gold = intersection(gold_boundary_index,input_boundary_index)
only_input = exclusion(input_boundary_index, input_gold)
only_gold = exclusion(gold_boundary_index, input_gold)
tp = len(input_gold)
fp = len(only_input)
fn = len(only_gold)
'''
print(input_gold)
print(only_input)
print(only_gold)
'''
precision = float(tp)/(tp + fp)
recall = float(tp)/(tp + fn)
f1 = 2 * (float(precision * recall) / (precision + recall))

print("en")
print("precision: " + str(precision))
print("recall: " + str(recall))
print("tp: " + str(tp))
print("fn: " + str(fn))
print("fp: " + str(fp))
print("f1: " + str(f1))
