#-*-coding:utf-8-*-

import requests
import lxml.html
import time
from pymongo import MongoClient
import random
import csv
import copy

class MongoScore:
    def __init__(self,client=None):
        self.client=MongoClient('localhost',27017)
        self.db=self.client.score


    def __getitem__(self,name):
        record=self.db.score.find_one({'name':name})
        if record:
            return record['admit']
        else:
            raise KeyError(name+'does not exist')
    def get_all(self):
        return self.db.score1w.find()

    def __setitem__(self,name,record):
        self.db.score.insert_one({'name':name,'admit':record})

    def update(self,name,record):
        self.db.score.update({'name':name},{'$set':{'admit':record}},upsert=True)

    def add_one(self,col):
        self.db.score1w.insert_one({'_id':col['name'],'admit':col['admit']})
    def add_seq(self,col):
        self.db.score1w_seq.insert_one({'_id':col['_id'],'admit':col['admit']})
def get_score(url):
    r=requests.get(url)
    print(r.url)
    if url!=r.url:
        return None
    r.encoding='utf-8'
#    print(r.apparent_encoding)
    tree=lxml.html.fromstring(r.text)
#    print(r.text)

    span=tree.cssselect('p.li-school-label>span')[0]
    coldict={}
    score_list=[]
    colName=span.text_content()
    trs=tree.cssselect('table>tbody>tr')
    for tr in trs:
        tds=tr.cssselect('td')
        
        if len(tds)>1:
            year=tds[0].text_content()
            high=tds[1].text_content()
            average=tds[2].text_content()
            low=tds[3].text_content()
            admit={'year':year,'high':high,'average':average,'low':low}
            score_list.append(admit)
    if len(score_list)>0:
        coldict={'name':colName,'admit':score_list}
        return coldict
    else:
        return None
# begin and end use to diffrent school code
def get_data():
    begin=280
    end=400
    hebei='10016'
    wenke='10034'
    like='10035'
    ms=MongoScore()
    for i in range(505,650):
        url='http://gkcx.eol.cn/schoolhtm/schoolAreaPoint/'+str(i)+'/'+hebei+'/'+wenke+'/10036.htm'
        try:
            result=get_score(url)
            if result:
                ms.add_one(result)
        except IndexError:
            print("%d error"%(i+begin))
        time.sleep(5+random.random()*10)

def get_order(filename):
    seq={}
    with open(filename,'r') as csvfile:
        reader=csv.reader(csvfile)
        for item in reader:
            seq[item[0]]=item[1]
    return seq


def add_order():
    torder={}    
    torder['2015']=get_order('2015w.csv')
    torder['2014']=get_order('2014w.csv')
    torder['2016']=get_order('2016w.csv')
    ms=MongoScore()
    enroll=ms.get_all()
    for uni in enroll:
        col=copy.deepcopy(uni)
        for ayear in col['admit']:
           if ayear['year'] in ['2016','2014','2015']:
#               if ayear['high']!='--':
#                  ayear['high_seq']=torder[ayear['year']][ayear['high'][:3]]          
                if ayear['average']!='--':
                   ayear['aver_seq']=torder[ayear['year']][ayear['average'][:3]]
                if ayear['low']!='--':
                   ayear['low_seq']=torder[ayear['year']][ayear['low'][:3]]
        ms.add_seq(col)
        print(col)

if __name__=='__main__':
    add_order()
