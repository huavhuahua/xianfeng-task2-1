
#!/usr/bin/python
# coding: utf-8

import requests
import re
import chardet
#link = "https://pvp.qq.com/web201605/herodetail/312.shtml"
#headers = {'User-Agent' : 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}

rex = '^<a herf="(herodetail)\/\d{3}\.shtml"'
r1 = requests.get("https://pvp.qq.com/web201605/herolist.shtml")
r1.encoding='ISO-8859-1'
after_gzip= r1.content
print(chardet.detect(after_gzip))
print(after_gzip.decode('GB2312'))
html = after_gzip.decode('GB2312')
with open('yuanma.txt',"a+") as f:
    f.write(html)
    f.close()

#html = after_gzip.decode('GB2312')
#r2 = re.findall(rex,html)
#print(r2)


