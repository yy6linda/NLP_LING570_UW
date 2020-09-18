import re
import sys
from sys import argv
import string

def word_evaluate(input_word, gold_word):
    m = len(input_word)
    n = len(gold_word)
    eval_mat =  [ [0]*(m+1) for t in range(n+1)]
    for j in range(0, m + 1):
        eval_mat[0][j] = j
    for i in range(0, n + 1):
        eval_mat[i][0] = i
    cost = 1
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if gold_word[i-1] == input_word[j-1]:
               replace_cost = 0
            else:
               replace_cost = 1
            eval_mat[i][j] = min(eval_mat[i - 1][j - 1]+replace_cost, eval_mat[i][j - 1] + cost, eval_mat[i - 1][j] + cost)
    return (eval_mat[i][j])

if __name__ == "__main__":

    i = 0
    cost = 0
    gold = sys.argv[1]
    with open(gold, 'r') as f:
       gold_line = f.readlines()
    for i_line in sys.stdin:
       g_line = gold_line[i]
       '''
       print("input")
       print(i_line)
       print("gold")
       print(g_line)
       print("******")
       '''
       cost = cost + word_evaluate(i_line, g_line)
       i = i + 1
    print(cost)
    
