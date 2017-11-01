#-*-coding:utf-8-*-

from pymongo import MongoClient

def get_aim(sub,school):
    client=MongoClient('localhost',27017)
    db=client.score
    if sub=='1':
        collection=db.score_seq
    else:
        collection=db.score1w_seq
    
    unis=collection.find({"_id":school})[0]
    for item in unis['admit']:
        if item['year'] in ('2016','2015','2014'):
            print('%s 年: 平均名次 %s'%(item['year'],item['aver_seq']))
            if item['low']!='--':
                print('%s 年: 最低名次 %s'%(item['year'],item['low_seq']))
if __name__=='__main__':
    sub=input('选择文科或理科:  1:理科  2:文科')
    school=input('输入学校:')

    get_aim(sub,school)
