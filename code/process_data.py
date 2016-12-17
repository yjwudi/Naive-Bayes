import os
import re
import codecs,sys
from collections import defaultdict

#数据文件夹路径
file_path = ['..\\data\\c1_atheism','..\\data\\c2_sci.crypt','..\\data\\c3_talk.politics.guns','..\\data\\c4_comp.sys.mac.hardware']
#数据标签
file_class = [0,1,2,3]


def my_token(line):
    s = re.findall("[A-Za-z]+",str.lower(str(line)))
    #s = line.split()
    return list(set(s))
def my_token_list(line):
    s = re.findall("[A-Za-z]+",str.lower(str(line)))
    #s = line.split()
    return list(s)
def get_word_map():
     #记录单词位置
    word_set = set()
    for f_path in file_path:
        #print(f_path)
        file_list = []
        for root,dirs,files in os.walk(f_path):
            for file_name in files:
                file_list.append(os.path.join(root,file_name))
        for file_name in file_list:
            file_object = open(file_name,'rb')
            try:
                 lines = file_object.read()
            finally:
                 file_object.close()
            #print(lines)
            line_word_list = my_token(lines)
            for word in line_word_list:
                word_set.add(word)
            #break
        #break
    #print(word_set)
    print("word_set length: ", len(word_set))
    word_idx_map = dict()
    vec_size = 1
    for word in word_set:
        #print(word)
        word_idx_map[word] = vec_size
        vec_size += 1
    return word_idx_map, vec_size
def get_data():
    word_idx_map,vec_size = get_word_map()
    #构造每个文件的向量，并对应标签
    txt_vec_list = []
    for i in range(0,len(file_path)):
        #print("i: ", i)
        f_path = file_path[i]
        label = file_class[i]
        file_list = []
        for root,dirs,files in os.walk(f_path):
            for file_name in files:
                file_list.append(os.path.join(root,file_name))
        for file_name in file_list:
            word_vec = [0]*vec_size
            file_object = open(file_name,'rb')
            try:
                 lines = file_object.read()
            finally:
                 file_object.close()
            #print(lines)
            line_word_list = my_token_list(lines)
            sum = 0
            for word in line_word_list:
                idx = word_idx_map[word]
                word_vec[idx] = 1
            word_vec.append(label)
            txt_vec_list.append(word_vec)
            #print(word_vec)
            #break
        #break
    return txt_vec_list