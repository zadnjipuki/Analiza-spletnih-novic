
__author__ = 'paula'
import Circos
import N_grams
import nltk
from nltk.collocations import *
import math

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

def add_coll(collocations,w1,w2):
    #if w2 =='jesti' or w2=='vlada':
    #   print('prej',collocations)
    #collocations[w1]=fix_dict(collocations[w1],w2)
    if w2 in collocations[w1]: collocations[w1][w2]+=1
    else: collocations[w1][w2]=1
    #if w1== 'janša': print('potem',collocations)
    return collocations

def preparation(text,window_size,wanted_list,collocations,words):

    window = text[0:window_size]
    window_wanted = {}

    for i in window:
        window_wanted = fix_wanted_dict(window_wanted,wanted_list,i)
        words = fix_dict(words,i)

    for i in window_wanted:
        for j in window:
            if i != j: collocations = add_coll(collocations, i, j)

    return window_wanted,words,collocations


#text is list of tokenized words (without stopwords, without rare words)
def count_collocations(text,window_size,wanted_list,collocations,words):
    window_wanted,words,collocations = preparation(text,window_size,wanted_list,collocations,words)

    i=1
    while len(text)-i >=window_size:
        window= text[i:i+window_size]
        new_word = text[i+window_size-1]
        window_wanted = fix_wanted_dict(window_wanted,wanted_list,new_word,text[i-1])

        i+=1
        words = fix_dict(words,new_word)

        for w in window_wanted:
            if w != new_word: collocations=add_coll(collocations, w, new_word)
            else:
                for k in window[:-1]:
                    collocations = add_coll(collocations, new_word, k)

    return collocations,words


def collocate(window_size,wanted_list,texts_include_words,year=''):
    collocations = {w: {} for w in wanted_list}
    words = {}
    num_words = 0
    rows = Circos.get_all_articles()
    texts = [N_grams.tokenize_words(t[1].lower()) for t in rows]

    for t in texts:
        num_words += len(t)
        collocations,words = count_collocations(t,window_size,wanted_list,collocations,words)

    print('Okno velikosti ',window_size,':')
    for c in collocations:
        print('Kolokacije z imenom ',c)
        for word in collocations[c]:
            if words[word]<50:
                collocations[c][word]=0
                continue
            col_number = collocations[c][word]

            pmi = math.log((col_number/(num_words-1))/(words[c] * words[word] / math.pow(num_words,2)))
            collocations[c][word]= pmi #(pmi,col_number)
        collocations[c] = sorted(collocations[c].items(), key=lambda x: x[1], reverse=True)
        print(collocations[c][:15])

    return collocations,words

#primer uporabe: collocate(velikost okna, sopojavitve s sledeöimi imeni)
collocate(20,['janša','jelinčič','erjavec','bush','putin','merklov','blair','berlusconi'],[],'')
collocate(5,['janša','jelinčič','erjavec','drnovšek','bush','putin','merklova','blair','berlusconi'],[],'')
collocate(10,['janša','jelinčič','erjavec','drnovšek','bush','putin','merklova','blair','berlusconi'],[],'')
collocate(20,['janša','jelinčič','erjavec','drnovšek','bush','putin','merklova','blair','berlusconi'],[],'')
collocate(40,['janša','jelinčič','erjavec','drnovšek','bush','putin','merklova','blair','berlusconi'],[],'')
collocate(50,['janša','jelinčič','erjavec','drnovšek','bush','putin','merklova','blair','berlusconi'],[],'')
collocate(60,['janša','jelinčič','erjavec','drnovšek','bush','putin','merklova','blair','berlusconi'],[],'')
#collocate(3,['janša'],['janš'],'2005')
#
