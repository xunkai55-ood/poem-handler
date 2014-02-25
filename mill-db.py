# -*- coding: utf-8 -*-

import codecs
import re
import json
import sqlite3

DEBUG = False

def fix(raw):
    rec = re.compile(u"（.*?）", re.DOTALL)
    half = rec.sub("", raw)
    rec = re.compile(r"&#[0-9]{1,10};")
    rst = rec.findall(half)
    if len(rst):
        for each in rst:
            num = int(each[2:-1])
            num_str = str(hex(num))[2:]
            half.replace(each, r"\u" + num_str)
    return half

def get_inner(line):
    rec = re.compile(r"'.*?'", re.DOTALL)
    try:
        x = rec.findall(line)[0]
    except:
        return ""
    else:
        return x[1:-1]

def db_start():
    
    conn = sqlite3.connect('_poem1402.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS poems 
                   (id integer primary key autoincrement, dynasty text, author text, subject text, poem text)''')
    return (conn, cur)

def db_close(conn):
    conn.commit()
    conn.close()

def db_write(cur, d, a, s, p):
    cur.execute('INSERT INTO poems (dynasty, author, subject, poem) VALUES(?,?,?,?)', [d, a, s, p])

def main(f):

    conn, cur = db_start()

    dynasty = ""
    author = ""
    subject = ""
    poem = ""
    cnt = 0

    for line in f:
        if line.find(u"<Dynasties>") >= 0:
            pass
        elif line.find(u"<Dynasty name") >= 0:
            dynasty = get_inner(line)
        elif line.find(u"<Authors>") >= 0:
            pass
        elif line.find(u"<Author name") >= 0:
            author = get_inner(line)
        elif line.find(u"<Poems>") >= 0:
            pass
        elif line.find(u"<Poem subject") >= 0:
            subject = get_inner(line)
        elif line.find(u"</Poem>") >= 0:
            db_write(cur, dynasty, author, subject, poem)
            poem = ""
            cnt += 1
            print cnt
            pass
        elif line.find(u"</Poems>") >= 0:
            pass
        elif line.find(u"</Author>") >= 0:
            pass
        elif line.find(u"</Authors>") >= 0:
            pass
        elif line.find(u"</Dynasty>") >= 0:
            pass
        elif line.find(u"</Dynasties>") >= 0:
            pass
        else:
            poem = poem + fix(line)

    db_close(conn)

if "__main__" == __name__:
    f = codecs.open("_poets.txt", "r", "utf-8")
    main(f)
