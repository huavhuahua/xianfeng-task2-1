import os
import requests
import chardet
import json
import  re
import pymysql


r1 = requests.get("https://pvp.qq.com/web201605/js/herolist.json")
a=r1.content.decode()
if a.startswith(u'\ufeff'):
    a = a.encode('utf8')[3:].decode('utf8')
herojson = json.loads(a)
print(herojson)
for thishero in herojson:
    r2 = requests.get('https://pvp.qq.com/web201605/herodetail/' + str(thishero['ename'] )+ '.shtml')
    r2.encoding = 'ISO-8859-1'
    after_gzip = r2.content
    html = after_gzip.decode('GB2312', 'ignore')
    print(html)
    yx = {}
    yx['id'] = re.search(
        r' <span class="hidden">(.*?)</span>',
        html, re.M | re.I).group(1)
    yx['name'] = re.search(r'cover-name">(.*?)</h2>', html, re.M | re.I).group(1)
    yx['bigname'] = re.search(r'cover-title">(.*?)</h3>', html, re.M | re.I).group(1)
    yx['shengcun'] = re.search(
        r'<span class="cover-list-bar data-bar1 fl"><b class="icon"></b><i class="ibar" style="width:(.*?)%"></i></span>',
        html, re.M | re.I).group(1)
    yx['gongji'] = re.search(
        r'<span class="cover-list-bar data-bar2 fl"><b class="icon"></b><i class="ibar" style="width:(.*?)%"></i></span>',
        html, re.M | re.I).group(1)
    yx['jinengxiaoguo'] = re.search(
        r'<span class="cover-list-bar data-bar3 fl"><b class="icon"></b><i class="ibar" style="width:(.*?)%"></i></span>',
        html, re.M | re.I).group(1)
    yx['shangshou'] = re.search(
        r'<span class="cover-list-bar data-bar4 fl"><b class="icon"></b><i class="ibar" style="width:(.*?)%"></i></span>',
        html, re.M | re.I).group(1)
    yx['bgpic'] = re.search(r'<div class="zk-con1 zk-con" style="background:url\(\'(.*?)\'\) center 0">', html,
                            re.M | re.I).group(1)

    jinengtu = re.search(r'<ul class="skill-u1">([\s\S]*) <li class="no5"', html, re.M | re.I).group(1)
    jinengpiclist = re.findall(r'<img src="(.*?)" alt=""', jinengtu, re.M | re.I)
    jineng = re.search(r'<div class="skill-show">([\s\S]*) <div class="sugg rs fl">', html, re.M | re.I).group(1)
    jinengnamelist = re.findall(r'<p class="skill-name"><b>(.*?)</b>', jineng, re.M | re.I)
    jinenglengquelist = re.findall(r'</b><span>(.*?)</span><span>', jineng, re.M | re.I)
    jinengxiaohaolist = re.findall(r'</span><span>(.*?)</span></p>', jineng, re.M | re.I)
    jinengdeclist = re.findall(r'<p class="skill-desc">(.*?)</p>', jineng, re.M | re.I)
    jinengtiplist = re.findall(r'<div class="skill-tips">(.*?)</div>', jineng, re.M | re.I)
    jinengid = re.findall(r'heroimg/\d{1,3}/(.*?).png', jinengtu, re.M | re.I)
    print(jinengtu)
    print(jinengid)
    for i in range(len(jinengdeclist)):
        jinengdeclist[i] = jinengdeclist[i].replace('<br>', '')
    for i in range(len(jinengtiplist)):
        jinengtiplist[i] = jinengtiplist[i].replace('<br>', '')

    jinengdic = {}
    jinengdic['name'] = jinengnamelist
    jinengdic['lengque'] = jinenglengquelist
    jinengdic['xiaohao'] = jinengxiaohaolist
    jinengdic['dec'] = jinengdeclist
    jinengdic['tip'] = jinengtiplist
    jinengdic['pic'] = jinengpiclist
    jinengdic['id'] = jinengid
    yx['jineng'] = jinengdic

    equip = re.search(r'<div class="equip-bd">([\s\S]*)  <div class="zk-con5 zk-con">', html, re.M | re.I).group(1)
    equipdata = re.findall(r'<ul class="equip-list fl" data-item="(.*?)">', equip, re.M | re.I)
    equiptip = re.findall(r'<p class="equip-tips">(.*?)</p>', equip, re.M | re.I)
    yxequip = {}
    yxequip['data'] = equipdata
    yxequip['tip'] = equiptip
    yx['equip'] = yxequip

    file = open(r'./herojson/' + yx['name'] + '.json', 'w', encoding='utf-8')
    file.write(str(yx))

    db = pymysql.connect("mysqlserver", "username", "password", "wzrytest")

    cursor = db.cursor()
    i = 0
    for jname in range(len(jinengdic['name']) - 1):

        sql = """INSERT INTO jinenglist(id,name,
                 lengque, xiaohao, dec1, tip , pic)
                 VALUES ('%d','%s', '%s', '%s', '%s', '%s','%s')""" % (
            int(jinengdic['id'][i]), jinengdic['name'][i], jinengdic['lengque'][i], jinengdic['xiaohao'][i],
            jinengdic['dec'][i], jinengdic['tip'][i], jinengdic['pic'][i])
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except:
            # 如果发生错误则回滚
            db.rollback()
        i = i + 1

    i = 0
    jinengdicstr = ''
    for jndic in jinengdic['id']:
        jinengdicstr = jinengdicstr + jndic + '|'

    equipdicstr = ''

    for xx in range(len(yxequip['data']) - 1):
        equipdicstr = equipdicstr + yxequip['data'][i] + 'x|x' + yxequip['tip'][i] + 'x|x'
        i = i + 1

    sql = """INSERT INTO herolist(id,name,
             bigname,shengcun ,gongji ,jinengxiaoguo  , shangshou,bgpic,jineng,equip)
             VALUES ('%d','%s', '%s', '%s', '%s', '%s','%s','%s','%s','%s')""" % (
        int(yx['id']), yx['name'], yx['bigname'], yx['shengcun'],
        yx['gongji'], yx['jinengxiaoguo'], yx['shangshou'], yx['bgpic'], jinengdicstr, equipdicstr)
    print(sql)
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        db.rollback()

    # 关闭数据库连接
    db.close()

'''
r1.encoding = 'ISO-8859-1'
after_gzip = r1.content
print(chardet.detect(after_gzip))
print(after_gzip.decode('GB2312'))
'''


