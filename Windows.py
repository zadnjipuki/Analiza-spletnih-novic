__author__ = 'paula'
import sqlite3
import datetime
from datetime import datetime as da
import time


def get_dates(start_date,end_date,period):
    dates= []
    start_date = da.strptime(start_date, '%Y-%m-%d')
    end_date = da.strptime(end_date, '%Y-%m-%d')
    date = start_date
    while date <= end_date:
        from_d = date
        to_d = date + datetime.timedelta(days=period)
        if to_d > end_date: to_d = end_date

        dates.append((from_d.strftime("%Y-%m-%d"),to_d.strftime("%Y-%m-%d")))
        date = to_d + datetime.timedelta(days=1)
    return dates

def get_windows(start_date,end_date,window_size,search):

    start_date = da.strptime(start_date,'%Y-%m-%d')
    end_date=da.strptime(end_date,'%Y-%m-%d')
    date = start_date
    windows = []
    time = []

    while date<=end_date:
        from_d= date
        to_d = date + datetime.timedelta(days=window_size)
        if to_d > end_date: to_d = end_date
     
        texts = get_texts(from_d,to_d,search)
        texts = join_texts(texts)
        windows +=[texts]
        #time += [from_d.strftime("%Y-%m-%d")]
        time += [from_d]
        date= to_d + datetime.timedelta(days=1)
    #texts = get_texts(start_date,end_date)
    
    return windows,time

def join_texts(texts):
    texts=" ".join(texts)
    return texts

def get_texts(start_date,end_date,search):
    
    db = sqlite3.connect('asi-database.sqlite')
    cursor = db.cursor()
    #statment = 'SELECT contents FROM asidata WHERE date >= \'%s\' and date <= \'%s\' and  contents like \'%%%s%%\''  %(start_date,end_date,search[0])
    statment = 'SELECT contents FROM asidata WHERE date >= \'%s\' and date <= \'%s\''  %(start_date,end_date)
    #for i in search[1:]: statment += 'or contents like \'%%%s%%\'' % i

    cursor.execute(statment)
    all_rows = cursor.fetchall()
    db.close()

    texts=[]
    for a in all_rows:
        text = a[0].lower()
        texts.append(text)

    return texts

