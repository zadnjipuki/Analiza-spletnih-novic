__author__ = 'paula'
import N_grams
import Windows
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(font_scale=2.2)
import numpy as np
from scipy.interpolate import interp1d
import random
import matplotlib.dates as mdates
import pandas as pd
import Smoothing
import datetime
from datetime import datetime as da

#da besed v oknih ni potrebno steti znova in znova, saj vcasih ne potrebujemo vseh besedil
besede = [6252, 25606, 65170, 69607, 65326, 69925, 69812, 73020, 75008, 86779, 115138, 114807, 94689, 82106, 42554, 92092, 122102, 117075, 110329, 110924, 112802, 97081, 76841, 100293, 107904, 116808, 97320, 87918, 104234, 95416, 86201, 122547, 115301, 115685, 115142, 113883, 122037, 99666, 116538, 111155, 114962, 117525, 119492, 106790, 72178, 36442, 112398, 125251, 123496, 121913, 106704, 121675, 123784, 131922, 129879, 130587, 119666, 104472, 126075, 128234, 102986, 134959, 126358, 131069, 138952, 144066, 150480, 112259, 126540, 141579, 125026, 124847, 126640, 120942, 123954, 131802, 142665, 143964, 160588, 152820, 155029, 152716, 152426, 131330, 156476, 159112, 158415, 154655, 149402, 149682, 115789, 75461, 149515, 143362, 145555, 148650, 124338, 146888, 143105, 136656, 150496, 145902, 164122, 135467, 131652, 115163, 95880, 124705, 130906, 127333, 123929, 129176, 137070, 133311, 123570, 128851, 121173, 134923, 99129, 114193, 145080, 140312, 149162, 149416, 143488, 151458, 153540, 147562, 136501, 101909, 142796, 155278, 138618, 137870, 138529, 134505, 81801, 68923, 125780, 141549, 131228, 147423, 115706, 140219, 126246, 139903, 135765, 134111, 157990, 136727, 181511, 174523, 139945, 225132, 217582, 206765, 214734, 210700, 211822, 187275, 215634, 178995, 178384, 178597, 169179, 141692, 163288, 184527, 183523, 167566, 182109, 183114, 183721, 171511, 190779, 128644, 197244, 193249, 181595, 168710, 188060, 184661, 129380, 101911, 184511, 198089, 183213, 193206, 210719, 198804, 206601, 206486, 214286, 220780, 172465, 220206, 215370, 159786, 153859, 206871, 210729, 225832, 187703, 213874, 225598, 201944, 225610, 202483, 227053, 203237, 206280, 172026, 209737, 245138, 223756, 216400, 211770, 250703, 260538, 221895, 230830, 169673, 215005, 243035, 261757, 246597, 250776, 221771, 155499, 172806, 242673, 251322, 238152, 225884, 253573, 265014, 251259, 191123, 252108, 261487, 263082, 267144, 207515, 233630, 174545, 253689, 267137, 251425, 234991, 260379, 195102, 248186, 237661, 242709, 242142, 225615, 170118, 167642, 220602, 262310, 261483, 251383, 267459, 276788, 263786, 238708, 260038, 239791, 252604, 230712, 273525, 276222, 283234, 210127, 161779, 188305, 272383, 243500, 259552, 277594, 261557, 276939, 273988, 278994, 293790, 302357, 274106, 228562, 314210, 241973, 277858, 294835, 282910, 252917, 279830, 275314, 254097, 270863, 246440, 176677, 238132, 224972, 242924, 235884, 227890, 289606, 291500, 298698, 281837, 243048, 301767, 286029, 313715, 259189, 284564, 318501, 309375, 325284, 315032, 261332, 238728, 251242, 336960, 373333, 371018, 307191, 357693, 353614, 369939, 365149, 378845, 326860, 375041, 365460, 352280, 255552, 217564, 134372, 329856, 354937, 321910, 333699, 283161, 274498, 300586, 198103, 290320, 297738, 242754, 202818, 298444, 326910, 386095, 398288, 381786, 353930, 375146, 333138, 1, 44354, 390696, 406750, 377652, 386288, 375483, 303282, 264649, 231964, 361767, 383193, 376883, 327124, 362936, 350898, 367972, 361892, 371807, 393837, 359503, 347623, 331471, 281717, 396234, 383541, 350549, 334804, 359835, 327242, 313997, 273571, 108748]

def group(wanted_list):
    groups = []
    counter = 0
    for i in wanted_list:
        groups.append([counter + m for m in range(len(i))])
        counter = counter + len(i)

    wanted_list = sum(wanted_list, [])

    return groups,wanted_list

def count_words(wanted_list,texts):
    slovarji = []
    for text in texts:         
         slovar = {i:0 for i in wanted_list}
         print('token start')
         number,words = N_grams.tokenize_words(text,wanted_list)
         print('token')
         for i in words:
              slovar[i]+=1
         slovarji.append(slovar)
    return slovarji

# n stands for n-grams
def calc_freq(date_from,date_to,window_size,wanted_list,n,search=[]):
    groups,wanted_list = group(wanted_list)
    # list of tuples of dates
    all_dates = Windows.get_dates(date_from,date_to,365)  # these are not windows, smaller problems
    # for dates and frequencies
    x = []
    y = np.empty((len(wanted_list), 0)).tolist()
    stevec = 0
    print('grem v zanke')
    for tup in all_dates:
        print('leto')
        windows, time = Windows.get_windows(tup[0], tup[1], window_size,search)
        print('windows')
        x += time
        if n==1: grams = count_words(wanted_list,windows)
        else: grams, words_per_window = N_grams.list_of_ngrams(windows, n)
        print('ngrami narjeni')
        for count, i in enumerate(grams):
            #words = words_per_window[count]  #to calculate frequency
            #besede.append(words)
            words =  besede[stevec]
            stevec+=1
            for j,wanted in enumerate(wanted_list):
                frequency = 0
                if wanted in i:
                    frequency = i[wanted] / words
                y[j].append(frequency)
        
        print('ngrami presteti')
    #print(besede)
    print('plotam')
    #print(x,y,wanted_list,groups)
            
    plot(x,y,wanted_list,groups)
    return x,y

def plot(x,y,wanted_list,groups):
    #print(x[0:5])
    #one graph for each group
    font = {'size': 13}
    plt.rc('font', **font)

    stevec = 0
    for g in groups:
        #if len(g) == 1: plt.plot(x, y[a])
        #else:
        for a in g:
            #plt.plot(x,y[a], label=wanted_list[a])
            yy = [1000000 * m for m in Smoothing.smoothTriangle(y[a],3)]
            el = yy[0]
            yy =  [el,el,el] + yy[:-3]
            #yy =   yy[3:-3]
            #word  = wanted_list[a][0].title() + ' ' + wanted_list[a][1].title()
            word = wanted_list[a].title()
            #if word == 'Dicaprio': word ='DiCaprio'
            #if wanted_list[a][1]=='hiv': word = 'Virus HIV'
            #plt.plot(x,yy,label=wanted_list[a].title())
            yy = yy[6:-10]
            xx = x[6:-10]
            print('lenx',len(x),'len y',len(yy))
            plt.plot(xx,yy,label = word)

        #plt.legend(bbox_to_anchor=(1, 1), loc=0, borderaxespad=1.)
        plt.legend(loc=1)
        if stevec==0:
            plt.text(datetime.datetime(2004, 8, 13, 0, 0), 0, ' |', fontsize=15,weight='heavy')
            plt.text(datetime.datetime(2004, 8, 13, 0, 0), -110,  'OI Atene',horizontalalignment='center', bbox=dict(facecolor='blue', alpha=0.1),size=23,style='italic',weight='light')
            plt.text(datetime.datetime(2000, 9, 15, 0, 0), 0, ' |', fontsize=15,weight='heavy')
            plt.text(datetime.datetime(2000, 9, 15, 0, 0), -110,  'OI Sydney',horizontalalignment='center', bbox=dict(facecolor='blue', alpha=0.1),size=23,style='italic',weight='light')
            plt.text(datetime.datetime(1998, 2, 7, 0, 0), 0, ' |', fontsize=15,weight='heavy')
            plt.text(datetime.datetime(1998, 2, 7, 0, 0), -110,  'OI Nagano',horizontalalignment='center', bbox=dict(facecolor='blue', alpha=0.1),size=23,style='italic',weight='light')
            plt.text(datetime.datetime(2006, 2, 10, 0, 0), 0, ' |', fontsize=15,weight='heavy')
            plt.text(datetime.datetime(2006, 2, 10, 0, 0), -110,  'OI Torino',horizontalalignment='center', bbox=dict(facecolor='blue', alpha=0.1),size=23,style='italic',weight='light')
            plt.text(datetime.datetime(2002, 2, 8, 0, 0), 0, ' |', fontsize=15,weight='heavy')
            plt.text(datetime.datetime(2002, 2, 8, 0, 0), -110,  'OI Salt Lake City',horizontalalignment='center', bbox=dict(facecolor='blue', alpha=0.1),size=23,style='italic',weight='light')
            plt.xlabel('Leto',labelpad=70)
        elif stevec==1:
            plt.text(datetime.datetime(2001, 1, 20, 0, 0), 0, ' |', fontsize=15,weight='heavy')
            plt.text(datetime.datetime(2001, 1, 20, 0, 0), -80,  'Izvolitev Busha',horizontalalignment='center', bbox=dict(facecolor='blue', alpha=0.1),size=23,style='italic',weight='light')
            plt.xlabel('Leto',labelpad=80)
        elif stevec==3:
            plt.text(datetime.datetime(2003, 3, 20, 0, 0), 0, ' |', fontsize=15,weight='heavy')
            plt.text(datetime.datetime(2003, 3, 20, 0, 0), -310,  'Invazija na Irak',horizontalalignment='center', bbox=dict(facecolor='blue', alpha=0.1),size=23,style='italic',weight='light')
            plt.text(datetime.datetime(2001, 10, 7, 0, 0), 0, ' |', fontsize=15,weight='heavy')
            plt.text(datetime.datetime(2001, 10, 7, 0, 0), -310,  'Invazija na Afganistan',horizontalalignment='center', bbox=dict(facecolor='blue', alpha=0.1),size=23,style='italic',weight='light')
            plt.xlabel('Leto',labelpad=100)

        elif stevec==20:
            plt.text(datetime.datetime(2001, 11, 23, 0, 0), 0, ' |', fontsize=15,weight='heavy')
            plt.text(datetime.datetime(2001, 11, 23, 0, 0), -75,  'Primer BSE v SLO',horizontalalignment='center', bbox=dict(facecolor='blue', alpha=0.1),size=23,style='italic',weight='light')
            plt.text(datetime.datetime(2006, 2, 12, 0, 0), 0, ' |', fontsize=15,weight='heavy')
            plt.text(datetime.datetime(2006, 2, 12, 0, 0), -75,  'Primer ptičje gripe v SLO ',horizontalalignment='right', bbox=dict(facecolor='blue', alpha=0.1),size=23,style='italic',weight='light')
            plt.xlabel('Leto',labelpad=75)  
        elif stevec==6:
            plt.text(datetime.datetime(2001, 9, 11, 0, 0), 0, ' |', fontsize=15,weight='heavy')
            plt.text(datetime.datetime(2001, 9, 11, 0, 0), -110,  '11. september',horizontalalignment='center', bbox=dict(facecolor='blue', alpha=0.1),size=23,style='italic',weight='light')
            plt.text(datetime.datetime(2004, 9, 3, 0, 0), 0, ' |', fontsize=15,weight='heavy')
            plt.text(datetime.datetime(2004, 9, 3, 0, 0), -145,  'Beslan',horizontalalignment='center', bbox=dict(facecolor='blue', alpha=0.1),size=23,style='italic',weight='light')
            plt.text(datetime.datetime(2004, 3, 11, 0, 0), 0, ' |', fontsize=15,weight='heavy')
            plt.text(datetime.datetime(2004, 3, 11, 0, 0), -110,  'Madrid',horizontalalignment='center', bbox=dict(facecolor='blue', alpha=0.1),size=23,style='italic',weight='light')
            plt.text(datetime.datetime(2005, 7, 7, 0, 0), 0, ' |', fontsize=15,weight='heavy')
            plt.text(datetime.datetime(2005, 7, 7, 0, 0), -110,  'London',horizontalalignment='center', bbox=dict(facecolor='blue', alpha=0.1),size=23,style='italic',weight='light')
            plt.text(datetime.datetime(2002, 10, 23, 0, 0), 0, ' |', fontsize=15,weight='heavy')
            plt.text(datetime.datetime(2002, 10, 23, 0, 0), -145,  'Moskva',horizontalalignment='left', bbox=dict(facecolor='blue', alpha=0.1),size=23,style='italic',weight='light')
            plt.text(datetime.datetime(2002, 10, 12, 0, 0), 0, ' |', fontsize=15,weight='heavy')
            plt.text(datetime.datetime(2002, 10, 12, 0, 0), -110,  'Bali',horizontalalignment='right', bbox=dict(facecolor='blue', alpha=0.1),size=23,style='italic',weight='light')
            plt.text(datetime.datetime(1998, 8, 7, 0, 0), 0, ' |', fontsize=15,weight='heavy')
            plt.text(datetime.datetime(1998, 8, 7, 0, 0), -110,  'Tanzanija',horizontalalignment='center', bbox=dict(facecolor='blue', alpha=0.1),size=23,style='italic',weight='light')
            plt.xlabel('Leto',labelpad=130)
        else:
            plt.xlabel('Leto',labelpad=0)
        #if stevec==4: plt.legend(loc=2)
        #else: plt.legend(loc=1)
        stevec+=1

        plt.gcf().autofmt_xdate()
        plt.ylabel('Število pojavitev na milijon besed',labelpad=50)
        #plt.xlabel('Leto',labelpad=20)

        plt.show()


#primer uporabe z 1-grami: calc_freq(od,do,seznami besed na istem prikazu,n)
x,y = calc_freq('1998-01-04','2006-07-08',7,[['olimpijski'],['bush','clinton'],['janša','jelinčič','erjavec'],['irak','afganistan'],['madonna','armstrong','papež','bush','pitt'],['nogomet','košarka','hokej'],['terorist']],1,[])

#primer uporabe z 2-grami
#x,y = calc_freq('1998-01-04','2006-07-08',7,[[('nore','krave'),('ptičja','gripa'),('virus','hiv')],[('svetlana','makarovič'),('milena','zupančič'),('boris','pahor'),('janez','lotrič')]],2)

