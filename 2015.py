#-*-coding:utf-8-*-
#pyhton3

import csv
import re


f=open('092710091586.txt','r')
lines=f.readlines()
f.close()
wr=csv.writer(open('2016w.csv','w')) 
for line in lines:
    span=re.match(r'^\d[\d \t]',line)
    if span:
#        line.split( )
        print(line)
        
        wr.writerow(line.split())

