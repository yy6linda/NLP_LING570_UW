import re
import sys
from sys import argv
import string
import os

'''
eg for train and test file: Pierre/NNP Vinken/NNP ,/, 61/CD years/NNS
featrues involved:containUC,containNum, containHyp, prevT
next2W,nextW,curW,prevTwoTags, suf, pref
'''

d_feature = dict()
d_kept_feat = dict()
d_feature['containUC'] = 0
d_feature['containNum'] = 0
d_feature['containHyp'] = 0
l_rare = list()
train_f = sys.argv[1]
test_f = sys.argv[2]
rare_thres = float(sys.argv[3])
feat_thres = float(sys.argv[4])
output_dir = sys.argv[5]
init_feats= open(output_dir+'/init_feats', 'w')
kept_feats= open(output_dir+'/kept_feats', 'w')
train_voc= open(output_dir+'/train_voc', 'w')
final_train_vectors= open(output_dir+'/final_train.vectors.txt','w')
final_test_vectors= open(output_dir+'/final_test.vectors.txt','w')

d_word = dict()

def contain_uc(word):
    return any(letter.isupper() for letter in word)

def contain_num(word):
    return any(letter.isdigit() for letter in word)

def contain_hyp(word):
    return any(letter == '-' for letter in word)

def rare_word(word):
    l_suf = []
    l_pref = []
    if len(word)>3:
        l_pref.append(word[:1])
        l_suf.append(word[:-1])
    if len(word)>4:
        l_pref.append(word[:2])
        l_suf.append(word[-2:])
    if len(word)>5:
        l_pref.append(word[:3])
        l_suf.append(word[-3:])
    if len(word)>6:
        l_pref.append(word[:4])
        l_suf.append(word[-4:])
    return l_pref, l_suf

with open(train_f, 'r') as f:
    for line in f:
        l_word = ['BOS','BOS']
        l_tag = ['BOS','BOS']
        line = line.strip('\n')
        words_line = line.split()
        for words in words_line:
            word = words.split("/")
            if "\/" in words:
                 new_word= ''.join(word[:2])
                 new_tag= word[2]
                 word[0] = new_word
                 word[1] = new_tag
            if word[0] in d_word and len( word[0])!=0:
                d_word[word[0]] = d_word[word[0]] + 1
            else:
                d_word[word[0]] = 1
            if len(word[0])!=0 and len(word[1])!=0:
                l_word.append(word[0])
                l_tag.append(word[1])
        l_word.extend(('EOS','EOS'))
        l_tag.extend(('EOS','EOS'))
        for i in range(2,len(l_word)-2):
            next2W = l_word[i+1]
            if 'next2W='+ next2W in d_feature:
                d_feature['next2W='+ next2W] = d_feature['next2W='+ next2W] + 1
            else:
                d_feature['next2W='+ next2W] = 1
            curW = l_word[i]
            if 'curW=' + curW in d_feature:
                d_feature['curW=' + curW] = d_feature['curW=' + curW] + 1
            else:
                d_feature['curW=' + curW] = 1
            prevW = l_word[i-1]
            if 'prevW='+ prevW in d_feature:
                d_feature['prevW='+ prevW] = d_feature['prevW='+ prevW] + 1
            else:
                d_feature['prevW='+ prevW] = 1
            nextW = l_word[i+1]
            if 'nextW='+ nextW in d_feature:
                d_feature['nextW='+ nextW] = d_feature['nextW='+ nextW] + 1
            else:
                d_feature['nextW='+ nextW] = 1
            prev2W  = l_word[i-2]
            if 'pre2W='+ prev2W in d_feature:
                d_feature['prev2W='+ prev2W] = d_feature['prev2W='+ prev2W] + 1
            else:
                d_feature['prev2W='+ prev2W] = 1
            prevTwoTags = l_tag[i-2] + '+' + l_tag[i-1]
            if 'prevTwoTags='+ prevTwoTags  in d_feature:
                d_feature['prevTwoTags='+ prevTwoTags] = d_feature['prevTwoTags='+ prevTwoTags] + 1
            else:
                d_feature['prevTwoTags='+ prevTwoTags] = 1
            prevT = l_tag[i-1]
            if 'prevT='+ prevT in d_feature:
                d_feature['prevT='+ prevT] = d_feature['prevT='+ prevT] + 1
            else:
                d_feature['prevT='+ prevT] = 1
    sorted_d_word = sorted(d_word.items(), key=lambda x:  (-1*x[1],  x[0]), reverse=False)
    for word in sorted_d_word:
        if word[1] > rare_thres:
            train_voc.write(word[0] + '    ' + str(word[1]) + '\n')
        else:
            if word[0] not in l_rare:
                l_rare.append(word[0])

    for word in l_rare:
        l_pref, l_suf = rare_word(word)
        for suf in l_suf:
            if 'suf='+ suf in d_feature:
                d_feature['suf='+ suf] = d_feature['suf='+ suf] + 1
            else:
                d_feature['suf='+ suf] = 1
        for pref in l_pref:
            if 'pref='+ pref in d_feature:
                d_feature['pref='+ pref] = d_feature['pref='+ pref] + 1
            else:
                d_feature['pref='+ pref] = 1

    sorted_d_feature = sorted(d_feature.items(), key=lambda x:  (-1*x[1],  x[0]), reverse=False)
    for feature in sorted_d_feature:
        init_feats.write(feature[0] + ' ' + str(feature[1])+'\n')
        if 'curW' in feature[0]:
            kept_feats.write(feature[0] + ' ' + str(feature[1])+'\n')
            d_kept_feat[feature[0]] = feature[1]
            continue
        if feature[1] > feat_thres:
            kept_feats.write(feature[0] + ' ' + str(feature[1])+'\n')
            d_kept_feat[feature[0]] = feature[1]
#print("#keep features")
#print(len(d_kept_feat))
#print("#allfeatures")
#print(len(d_feature))
'''create vectors'''
def create_vectors(input,output):
    with open(input, 'r') as f:
        n_line = 0
        for line in f:
            n_line = n_line + 1
            l_word = ['BOS','BOS']
            l_tag = ['BOS','BOS']
            line = line.strip('\n')
            words_line = line.split()
            for words in words_line:
                word = words.split("/")
                if "\/" in words:
                     #print(word)
                     new_word= ''.join(word[:2])
                     new_tag= word[2]
                     word[0] = new_word
                     word[1] = new_tag
                if len(word[0])!=0 and len(word[1])!=0:
                    l_word.append(word[0])
                    l_tag.append(word[1])
            l_word.extend(('EOS','EOS'))
            l_tag.extend(('EOS','EOS'))
            n_word = -1
            for i in range(2,len(l_word)-2):
                n_word = n_word + 1
                line = ''
                line = line + str(n_line)+'-'+str(n_word)+'-'+l_word[i] + ' ' + l_tag[i]
                curW = l_word[i]
                if 'curW='+ curW in d_kept_feat:
                    line = line + ' curW='+ curW + ' 1'
                prevW = l_word[i-1]
                if 'prevW='+ prevW in d_kept_feat:
                    line = line + ' prevW='+ prevW + ' 1'
                prev2W = l_word[i-2]
                if 'prev2W='+ prev2W in d_kept_feat:
                    line = line + ' prev2W='+ prev2W + ' 1'
                nextW = l_word[i+1]
                if 'nextW='+ nextW in d_kept_feat:
                    line = line + ' nextW='+ nextW + ' 1'
                next2W = l_word[i+2]
                if 'next2W='+ next2W in d_kept_feat:
                    line = line + ' next2W='+ next2W + ' 1'
                prevT = l_tag[i-1]
                if 'prevT='+ prevT in d_kept_feat:
                    line = line + ' prevT='+ prevT
                prevTwoTags = l_tag[i-2] + '+' + l_tag[i-1]
                if 'prevTwoTags='+ prevTwoTags  in d_kept_feat:
                    line = line +' prevTwoTags='+ prevTwoTags + ' 1'
                if contain_uc(curW):
                    line = line +' containUC 1'
                if contain_num(curW):
                    line = line +' containNum 1'
                if contain_hyp(curW):
                    line = line +' containHyp 1'
                if curW in l_rare:
                    l_pref, l_suf = rare_word(curW)
                    for pref in l_pref:
                        if 'pref='+ pref in d_kept_feat:
                            line = line +' pref='+ pref + ' 1'
                    for suf in l_suf:
                        if 'suf='+ suf in d_kept_feat:
                            line = line +' suf='+ suf + ' 1'
                line = line +'\n'
                line = line.replace(',', 'comma')
                output.write(line)
create_vectors(train_f,final_train_vectors)
create_vectors(test_f,final_test_vectors)
'''for running mallet'''
'''
train_vec = os.path.join(output_dir,"final_train.vectors.txt")
out_train_vec = os.path.join(output_dir, "final_train.vectors")
test_vec = os.path.join(output_dir,"final_test.vectors.txt")
out_test_vec = os.path.join(output_dir,"final_test.vectors")
me_model = os.path.join(output_dir,"me_model")
me_model_stdout = os.path.join(output_dir,"me_model.stdout")
me_model_stderr = os.path.join(output_dir,"me_model.stderr")
sys_out = os.path.join(output_dir,"sys_out")
os.system("mallet import-file --input "+train_vec+" --output "+out_train_vec)
os.system("mallet import-file --input "+test_vec+" --output "+out_test_vec+" --use-pipe-from "+out_train_vec)
os.system("mallet train-classifier --trainer MaxEnt --input "+out_train_vec+" --output-classifier "+me_model+" 1>"+me_model_stdout+" 2>"+me_model_stderr)
os.system("mallet classify-file --input "+test_vec+" --classifier "+me_model+" --output "+sys_out)
os.system("vectors2classify --training-file " + out_train_vec+" --testing-file "+out_test_vec+ " --trainer MaxEnt > "+ me_model_stdout+" 2> "+ me_model_stderr+" --output-classifier "+me_model)
'''
