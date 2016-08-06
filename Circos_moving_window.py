__author__ = 'paula'

__author__ = 'paula'
import Circos
import N_grams
import nltk
from nltk.collocations import *
import math
import numpy as np

dict_rev1={}
dict_rev2={}

def list_to_dict(l):
    return {l[i]:i for i in range(len(l))}

def refresh_matrix(matrix,word1,word2,dict1,dict2,num):
    a = dict1[word1]
    b = dict2[word2]
    matrix[a][b]+=num
    return matrix

#dodam w1 ce je potrebno in izbrisem w2 ce je potrebno
def fix_dict(dict,w1,w2=''):
    if w1 != '':
        if w1 in dict: dict[w1]+=1
        else: dict[w1]=1

    if w2=='': return dict
    dict[w2]-=1
    if dict[w2]==0: del dict[w2]
    return dict

def fix_wanted_dict(dict,wanted_list,w1,w2=''):
    if w1 not in wanted_list: w1=''
    if w2 not in wanted_list: w2=''
    if w1 == w2: return dict # npr ce nobena ni v wanted_list
    return fix_dict(dict,w1,w2)



def preparation(dict1,dict2,text,window_size,wanted_list1,wanted_list2,matrix):

    window = text[0:window_size]

    window_wanted1 = {}
    window_wanted2 = {}

    for i in window:
        window_wanted1 = fix_wanted_dict(window_wanted1,wanted_list1,i)
        window_wanted2 = fix_wanted_dict(window_wanted2,wanted_list2,i)

    for i in window_wanted1:
        num1 = window_wanted1[i]
        for j in window_wanted2:
            num2 = window_wanted2[j]
            num = num1 * num2
            matrix = refresh_matrix(matrix,i,j,dict1,dict2,num)

    return matrix,window_wanted1,window_wanted2


#text is list of tokenized words (without stopwords, without rare words)
def count_collocations(dict1,dict2,text,window_size,wanted_list1,wanted_list2,matrix):
    matrix,window_wanted1,window_wanted2 = preparation(dict1,dict2,text,window_size,wanted_list1,wanted_list2,matrix)
    end = False

    i=1
    while i<len(text):
        if i+window_size < len(text)-1: window= text[i:i+window_size]
        else:
            window = text[i:len(text)]
            end = True
        new_word = window[-1]

        window_wanted1 = fix_wanted_dict(window_wanted1,wanted_list1,new_word,text[i-1])
        window_wanted2 = fix_wanted_dict(window_wanted2,wanted_list2,new_word,text[i-1])

        i+=1


        if new_word in wanted_list1:
            for w in window_wanted2:
                matrix = refresh_matrix(matrix,new_word,w,dict1,dict2,window_wanted2[w])

        if new_word in wanted_list2:
            for w in window_wanted1:
                matrix = refresh_matrix(matrix,w,new_word,dict1,dict2,window_wanted1[w])

        if end: break

    return matrix
def reverse_dict(dict):
    return {v: k for k, v in dict.items()}

def sievov_diagram(matrix,dict1,dict2):
    rev1 = reverse_dict(dict1)
    rev2 = reverse_dict(dict2)

    f = open('workfile.txt','w')
    for i in range(len(dict1)):
        for j in range(len(dict2)):
            text = rev1[i].title() + '\t' + rev2[j].title() + '\n'
            for m in range(int(matrix[i][j])):f.write(text)

    #f.write('hi there\n') # python will convert \n to os.linesep
    f.close()

def collocate(window_size,wanted_list1,wanted_list2,key_words=[],year=''):
    print(key_words)
    rows = Circos.get_wanted_articles(key_words)
    texts = [N_grams.tokenize_words(t[1].lower()) for t in rows]


    matrix = np.zeros((len(wanted_list1),len(wanted_list2)))
    dict1 = list_to_dict(wanted_list1)
    dict2 = list_to_dict(wanted_list2)

    for t in texts:
        matrix = count_collocations(dict1,dict2,t,window_size,wanted_list1,wanted_list2,matrix)

    #print(matrix)
    sievov_diagram(matrix,dict1,dict2)
    matrix = matrix.astype(int)
    print(matrix)
    print('-',end=",")
    print(*wanted_list2, sep=',')
    for i,a in enumerate(matrix):
        print(wanted_list1[i],end=",")
        print(*a, sep=',')
    return matrix

#primeri uporabe: collocate(velikost okna, 1 sezbnam, drugi seznam,isci le v besedilih z vsebovanimi besedami)
#1
#collocate(100,['janša','bush','berlusconi','merklov','putin'],['cerkev','vojen','islam','nafta','terorist'],'')
#2
#collocate(100,['blair','bush','berlusconi','merklov','putin'],['blair','bush','berlusconi','merklov','putin'],['bush','berlusconi','merk','putin'])
#3
#collocate(100,['janša','erjavec','jelinčič','petereti','kučan','drnovšek'],['referendum','neodvisnost','evro','romi','cerkev','izbrisani','lustracija','komunizem'],['janš','erjav','jelinčič','peterl','kučan','drnovš'])
#collocate(100,['janša','erjavec','jelinčič','petereti','drnovšek','rode','kučan'],['janša','erjavec','jelinčič','petereti','drnovšek','rode','kučan'],['janš','erjav','jelinčič','peterl','rode','drnovš','kučan'])
#collocate(100,['einstein','hawking','newton','tesla'],['znanost','tehnologija','fizika','vesolje','bomba'],['einstein','hawking','newton','tesla'])
#collocate(100,['bono','opeka','križnar','mandela','terezija'],['afrika','otrok','šola','slaven','dobrodelen','pomoč','cerkev'],['bono','pedro','križnar','mandel','terez','opek'],'')
#collocate(100,['maze','armstrong','čeplak','schumacher','ronaldinho','mankoč','osovnikar','petkovšek','maradona','phelps'],['doping','lovorika','olimpijski',$
#collocate(100,['maze','armstrong','schumacher','ronaldinho','mankoč','osovnikar','petkovšek','maradona',],['doping','olimpijski','poškodba','zmaga'],['maze','armstrong','čeplak','schumacher','ronaldinh','mankoč','osovnikar','petkovš','maradon','phelps'])
#print_matrix_result('',['janša','bush','berlusconi','merkel','putin'],['eu','cerkev','zda','vojen','isla','rusija','nafta','teroristi'],100)
#collocate(100,['janša','bush','berlusconi','putin'],['cerkev','vojen','islam','orožje','nafta','terorist'],['janš','bush','berluscon','merk','putin'])
#collocate(100,['miloševič','bush','putin','berlusconi','janša'],['miloševič','vlada','in','v','so'],'')
"""
#collocate(5,['janša','jelinčič','erjavec','drnovšek','bush','putin','merklova','blair','berlusconi'],[],'')
#collocate(10,['janša','jelinčič','erjavec','drnovšek','bush','putin','merklova','blair','berlusconi'],[],'')
#collocate(20,['janša','jelinčič','erjavec','drnovšek','bush','putin','merklova','blair','berlusconi'],[],'')
#collocate(40,['janša','jelinčič','erjavec','drnovšek','bush','putin','merklova','blair','berlusconi'],[],'')
#collocate(50,['janša','jelinčič','erjavec','drnovšek','bush','putin','merklova','blair','berlusconi'],[],'')
#collocate(60,['janša','jelinčič','erjavec','drnovšek','bush','putin','merklova','blair','berlusconi'],[],'')
#collocate(3,['janša'],['janš'],'2005')
#

"""
