import re
#import nltk
import sqlite3
#from unidecode import unidecode
import sys
from nltk.tokenize import RegexpTokenizer, word_tokenize
from nltk.util import ngrams
import math
import lemmagen.lemmatizer
from lemmagen.lemmatizer import Lemmatizer
from itertools import chain

lemmatizer = Lemmatizer(dictionary=lemmagen.DICTIONARY_SLOVENE)

stopwords = []

 
def count_ngrams(grams):
    ngrams_dict = {}
    for gram in grams: add_gram(gram,ngrams_dict)
    return ngrams_dict
lemma_dict = {'madonna':'madonna','madonni':'madonna','pitt':'pitt','pittu':'pitt','bush':'bush','busha':'bush','bushu':'bush','bushem':'bush','clinton':'clinton','clintonu':'clinton','clintonom':'clinton','clintona':'clinton','terorizem':'terorist','teroristični':'terorist','teroristom':'terorist','terorizmu':'terorist','teroristi':'terorist',}

def build_ngrams(text, n, punctuation,avoide = True,including=[]):
    number,words = tokenize_words(text,punctuation)
            #if w not in lemma_dict: words.append( lemmatizer.lemmatize(w))
    grams = list(ngrams(words,n))
    if n==1: grams = list(chain(*grams))
    return grams,number
 

def add_gram(gram,dict):
    if gram in dict:
        dict[gram] += 1
    else:
        dict[gram] = 1
    return dict
         


# tokenizing to words, removing punctuation if punctuation==False
def tokenize_words(text,wanted,punctuation=False):
    text= re.sub("\d+", "", text) # gets read of numbers
    #if punctuation: return word_tokenize(text)
    tokenizer = RegexpTokenizer(r'\w+')
    r = tokenizer.tokenize(text)
    #return r
    result = []
    for w in r:

       # if w in stopwords: continue
         #lemma_dict = {'nore':'nore','norih':'nore','krave':'krave','krav':'krave','ptičja':'ptičja','ptičje':'ptičja','gripa':'gripa','gripe':'gripa','virus':'virus','virusu':'virus','virusa':'virus','virusom':'virus','hiv':'hiv'}
         if w in lemma_dict:  w=lemma_dict[w]
         else: w = lemmatizer.lemmatize(w) # nekatere besede se napacno lematizirajo, zato jih ne
         if w in wanted: result.append(w)
         #result.append(w)
    return len(r),result

# to rabim za words timelines, mi vrne list n-gramov
def list_of_ngrams(texts,n=1,punctuation = False,avoide= False,including=[]):
    grams = []
    words_per_window=[]
    for row in texts:
        n_grams = build_ngrams(row,n,punctuation,avoide,including)
        grams += [count_ngrams(n_grams[0])] # row[1] - column where actual article is saved
        words_per_window.append(n_grams[1])

    #grams = [sorted(i.items(), key=lambda x: x[1],reverse=True) for i in grams]

    return grams,words_per_window

def prepare_stop():
    for line in open('stop-words-slo', 'r', encoding='utf-8'):
        stopwords.append('')
        stopwords.append(line.strip('\n'))

#prepare_stop()
#lemma_dict ={'madonna':'madonna','madonni':'madonna','pitt':'pitt','pittu':'pitt','google':'google','googlu':'googel','youtube':'youtube','youtubu':'youtube','tesla':'tesla','gates':'gates','bono':'bono','mandela':'mandela','tereza':'terezija','tereze':'terezije','maze':'maze','ronaldinho':'ronaldinho','maradona':'maradona','schumacher':'schumacher','pribežniki':'prebežnik','begunci':'prebežnik','ilegalci':'prebežnik','migranti':'prebežnik','evro':'evro','nasa':'nasa','nasi':'nasa','blair':'blair','youtube':'youtub','čeplak':'čeplak','kaida':'kaida','kaidi':'kaida','eu':'eu','zda':'zda','bush':'bush','merkel':'merklov','berlusconi':'berlusconi','berlusconijem':'berlusconi','berlusconiju':'berlusconi','berlusconija':'berlusconi','eu':'eu','terorizem':'terorist','putin':'putin','putina':'putin','islam':'islam','islama':'islam','islamisti':'islam','naftni':'nafta','naften':'nafta'}
#lemma_dict = {'svetlana':'svetlana','svetlani':'svetlana','svetlano':'svatlana','svetlane':'svetlana','milena':'milena','milene':'milena','mileni':'milena','mileno':'milena','pahorja':'pahor','pahorju':'pahor','pahorjem':'pahor','tone':'tone','toneta':'tone','lotrič':'lotrič'}
#lemma_dict = {'bush':'bush','busha':'bush','bushu':'bush','bushem':'bush','clinton':'clinton','clintonu':'clinton','clintonom':'clinton','clintona':'clinton'}
#lemma_dict = {'terorizem':'terorist','teroristični':'terorist','teroristom':'terorist','terorizmu':'terorist','teroristi':'terorist'}