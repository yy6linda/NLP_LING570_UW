import re
import sys
from sys import argv
import string
'''convert input and gold to "tooo" type, where "t" stands for the start of a token,
"o" for inside of a token, white space is not counted'''
processed_input = ""
for line in sys.stdin:
    for word in line.split():
        processed_word = "t" + "o" * (len(word)-1)
        processed_input = processed_input + processed_word
#print(processed_input)
processed_gold = ""
gold = sys.argv[1]
with open(gold, 'r') as f:
    for line in f:
        for word in line.split():
            processed_word = "t" + "o" * (len(word)-1)
            processed_gold = processed_gold + processed_word
#print(processed_gold)
#print(len(processed_gold))
'''find the index for "t" '''
def find(str, ch):
    for i, ltr in enumerate(str):
        if ltr == ch:
            yield i
gold_boundary_index = list(find(processed_gold, "t"))
gold_boundary_index.append(len(processed_gold) - 1)
#print(gold_boundary_index)
input_boundary_index = list(find(processed_input, "t"))
input_boundary_index.append(len(processed_input) - 1)
#print(input_boundary_index)
'''return the index for "t" '''
gold_boundary_index = [ str(i) for i in gold_boundary_index ]
input_boundary_index = [ str(i) for i in input_boundary_index ]
'''using to index to represent a token'''
matched_gold = []
for i in range(0,len(gold_boundary_index)-1):
    match = gold_boundary_index[i] + "-" + gold_boundary_index[i + 1]
    matched_gold.append(match)
#print(matched_gold)
matched_input = []
for i in range(0,len(input_boundary_index)-1):
    match = input_boundary_index[i] + "-" + input_boundary_index[i + 1]
    matched_input.append(match)
#print(matched_input)
def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3
def exclusion(lst1, lst2):
    lst3 = [value for value in lst1 if value not in lst2]
    return lst3
input_gold = intersection(matched_input, matched_gold)
only_input = exclusion(matched_input, input_gold)
only_gold = exclusion(matched_gold, input_gold)
tp = len(input_gold)
fp = len(only_input)
fn = len(only_gold)
precision = float(tp)/(tp + fp)
recall = float(tp)/(tp + fn)
f1 = 2*(float(precision * recall) / (precision + recall))
'''
print("precision: " + str(precision))
print("recall: " + str(recall))
print("tp: " + str(tp))
print("fn: " + str(fn))
print("fp: " + str(fp))
print("f1: " + str(f1))
print(len(processed_gold))
print(len(processed_input))
'''
print(f1)
