#-*-coding:utf-8-*-
# python3

import requests
import csv
import lxml.html


r=requests.get('http://edu.sina.com.cn/gaokao/2014-06-24/1524425188.shtml')
tree=lxml.html.fromstring(r.text)
wr=csv.writer(open('2014.csv','w'))
trs=tree.cssselect('table>tbody>tr')
for tr in trs:
    tds=tr.cssselect('td')
    row=[]
    for td in tds:
        row.append(td.text_content())
    wr.writerow(row)


