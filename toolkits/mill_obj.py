# -*- coding: utf-8 -*-

import codecs
import re
import json
import sqlite3

DEBUG = False

def fix(half):
    rec = re.compile(r"&#[0-9]{1,10};")
    rst = rec.findall(half)
    if len(rst):
        for each in rst:
            num = int(each[2:-1])
            half = half.replace(each, unichr(num))
    return half

def fix2(raw):
    rec = re.compile(u"（.*?）", re.DOTALL)
    half = rec.sub("", raw)
    rec = re.compile(r"&#[0-9]{1,10};")
    rst = rec.findall(half)
    if len(rst):
        for each in rst:
            num = int(each[2:-1])
            if num >= 0x2C00:
                half = half.replace(each, unichr(num))
            else:
                half = half.replace(each, "")
    rst = u""
    for each in half:
        if each >= u'\U00002C00':
            rst += each
    return rst

def get_inner(line):
    rec = re.compile(r"'.*?'", re.DOTALL)
    try:
        x = rec.findall(line)[0]
    except:
        return ""
    else:
        return x[1:-1]

def create_object(d, a, s, p):
    rst = {}
    rst["dynasty"] = d
    rst["author"] = a
    rst["subject"] = s
    rst["poem"] = p

    return rst

def main(f):

    tf = codecs.open("_poets_obj_test.txt", "w", "utf-8")
    dynasty = ""
    author = ""
    subject = ""
    poem = ""
    cnt = 0

    for raw_line in f:
        line = fix(raw_line)
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
            cnt += 1
            subject = get_inner(line)
            print cnt
        elif line.find(u"</Poem>") >= 0:
            obj = create_object(dynasty, author, subject, poem)
            if DEBUG:
                print json.dumps(obj, ensure_ascii = False)
                tmp = input("ok")
            else:
                tf.write(json.dumps(obj, ensure_ascii = False))
                #db_write(obj)
            poem = ""
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
            poem = poem + fix2(raw_line)

if "__main__" == __name__:
    f = codecs.open("_poets_test.txt", "r", "utf-8")
    main(f)
