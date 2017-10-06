#-*-coding:utf-8-*-

from pymongo import MongoClient

def get_aim(seq):
    ranking=int(seq)
    client=MongoClient('localhost',27017)
    db=client.score
    unis=db.score_seq.find()
    aver_seq={}
    for uni in unis:
        total=0
        times=0
        for ayear in uni['admit']:
            if ayear['year'] in ('2016','2015','2014'):
                if ayear['average']!='--':
                    total+=int(ayear['aver_seq'])
                    times+=1
        if times!=0:
            aver_seq[uni['_id']]=total/times
    for item in aver_seq:
        aver_seq[item]=abs(int(aver_seq[item])-ranking)
    
    temp_l=sorted([[v[1],v[0]] for v in aver_seq.items()])
    aims=temp_l[:20]
    for aim in aims:
        col=db.score_seq.find({'_id':aim[1]})
        print("%s\n%s"%(col[0]['_id'], col[0]['admit']))

if __name__=='__main__':
    seq=input('Please input seqence:')
    get_aim(seq)
