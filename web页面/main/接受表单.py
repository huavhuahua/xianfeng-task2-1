from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap
import pymysql
from flask import request
import re

app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route('/')
def init():
    return render_template('a.html', a=' ')


@app.route('/result', methods=['POST'])
def result():
    print(request.form['search'])

    heroname = request.form['search']
    if (heroname == ''):
        error = 1
        return (render_template('search.html'))
    conn = pymysql.connect("188.131.175.223", "username", "password", "wzrytest", charset='utf8')
    cur = conn.cursor()
    sql1 = r"SELECT * FROM herolist where name like '%" + heroname + "%'"
    cur.execute(sql1)
    u1 = cur.fetchall()

    i=u1[0][8].split("|")
    jn=[]
    for j in i:
        sql2 = r"select * from jinenglist where id='"+j+"'"
        cur.execute(sql2)
        u2 = cur.fetchall()
        jn.append(u2)
    conn.close()
    print(u1[0])

    return render_template('fb.html', hero=u1[0], jineng1=jn[0],jineng2=jn[1],jineng3=jn[2],jineng4=jn[3])
    print(hero)

if __name__ == '__main__':
    app.run(host='localhost', debug=True)
