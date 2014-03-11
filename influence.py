# -*- encoding: utf-8 -*-

#######################################
# influence.py
# This code is aimed to assess each poem an influence value.
#######################################

from __future__ import division

from zpd import ZPD
from functions import is_chinese, is_simple_chinese

class Assessor():
    'Abstract class of assessors.'
    
    def assess(poem):
        return 0

IG_D = -40

import urllib
import urllib2
import re
import zlib
import os

DEBUG = 0

class BaiduAssessor(Assessor):
    'Assessor using a search-based method.'
    
    target_url = "http://www.baidu.com/s?wd="
    rec = re.compile("百度为您找到相关结果(.*?)个")
    #rec = re.compile((u"百度为您找到相关结果(.*?)个").encode("gbk"))
    req_header = {
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip,deflate,sdch', 
            'Accept-Language':'zh-CN,zh;q=0.8,ru;q=0.6,zh-TW;q=0.4,en;q=0.2',
            'Connection':'keep-alive', 
            'Host':'www.baidu.com',
            'Cookie':'BAIDUID=B8500BBB79E8FDF6563EA2C212264EA8:FG=1; bdshare_firstime=1384009474193; NBID=C0F11DCE8CED3FABDA7D2D3ADD5729EB:FG=1; MCITY=-%3A; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; BDRCVFR[fBLL8ZbbiMm]=I67x6TjHwwYf0; H_PS_TIPFLAG=O; H_PS_TIPCOUNT=1; BD_CK_SAM=1; H_PS_PSSID=5066_1435_5223_5213_5378_5369_4264_4759_5402_5342'
    }
    if DEBUG:
        httpHandler = urllib2.HTTPHandler(debuglevel=1)
        httpsHandler = urllib2.HTTPSHandler(debuglevel=1)
        opener = urllib2.build_opener(httpHandler, httpsHandler)
        urllib2.install_opener(opener)

    def __init__(self):
        self.input_cookies()

    def input_cookies(self):
        #s = raw_input("Copy cookies here = ")
        #self.req_header["Cookie"] = s
        if raw_input("Enter when cookie ready") == 'q':
            return
        else:
            f = open("__cookies.txt", "r")
            self.req_header["Cookie"] = f.read()
            f.close()
            return

    def to_query_style(self, u_str, minchar = 10, maxchar = 12):
        rst = u""
        cnt = 0
        for each in u_str:
            if cnt == maxchar:
                break
            elif is_simple_chinese(each):
                rst += each
                cnt += 1
            elif cnt < minchar:
                rst += u" "
            else:
                break
        return rst

    def to_query_url(self, query_str, ac = False):
        '''ac = True to search more accurately'''

        if not ac:
            return self.target_url + urllib.quote(query_str.encode('utf-8'))
        else:
            return self.target_url + '"' + urllib.quote(query_str.encode('utf-8')) + '"'

    def get_rr_number(self, url, recv = 0, is_zero = False):

        if (not is_zero and recv >= 4):
            return -1
        if (is_zero and recv >= 3):
            return 0
        try:
            req = urllib2.Request(url, None, self.req_header)
            response = urllib2.urlopen(req, timeout = 5)
        
            text = zlib.decompress(response.read(), 16 + zlib.MAX_WBITS)
            
        except:
            return self.get_rr_number(url, recv + 1)

        if (response.geturl() != url):
            print "WE'RE DETECTED, Cookie="
            self.input_cookies()

        rst = self.rec.findall(text)
        if len(rst) == 0:
            return self.get_rr_number(url, recv + 1, True)
        else:
            raw = rst[-1]
            i = 0
            while raw[i].isdigit() == False:
                i += 1
            
            raw = raw[i:].replace(",", "")
            return int(raw)

    def render(self, scores):
        if scores[0] == -1:
            return -1
        if scores[1] < 50 * scores[0]:
            return scores[1]
        else:
            return int((scores[0] * scores[1]) ** 0.5)

    def assess(self, poem_dic, ignore_dynasties = []):

        subject = poem_dic["subject"]
        poem = poem_dic["poem"]
        
        if poem_dic["dynasty"] in ignore_dynasties:
            return (IG_D, IG_D, IG_D)

        query_str = self.to_query_style(subject, 2) + u' ' + self.to_query_style(poem, 7, 20)
        print query_str
        full_url = self.to_query_url(query_str)
        a = self.get_rr_number(full_url)

        query_str = self.to_query_style(poem, 10, 20)
        full_url = self.to_query_url(query_str)
        b = self.get_rr_number(full_url)

        query_str = self.to_query_style(poem, 10, 20)
        full_url = self.to_query_url(query_str, True)
        c = self.get_rr_number(full_url)

        return (a, b, c)

def test():
    zpd = ZPD()
    bAssessor = BaiduAssessor()
    while True:
        poem_tup = zpd.pick(1)[0]
        poem_dic = zpd.tuple2dict(poem_tup)
        t = bAssessor.assess(poem_dic)
        k = 0
        while t == -1 and k < 3:
            k += 1
            t = bAssessor.assess(poem_dic)
        print t

def main_scan():
    zpd = ZPD()
    bAssessor = BaiduAssessor()
    
    step = 500
    n = zpd.count_all()
    start = input("give me your start point (0 ~ 860)")
    end = input("and end point (1 ~ 861)")
    
    if (start >= end):
        return

    ig_dynasties = [u'\u5143', u'\u660e']

    for i in range(start, end):
        if i != start:
            if os.path.exists("socres/score" + str(i) + ".txt"):
                print "cracked! exit"
                return
        print "============================================"
        print "work on : " + str(i * 500 + 1) + " / " + str(n)
        poems = zpd.select_by_id(i * 500, (i + 1) * 500)
        updates = []
        for each in poems:
            poem_dic = zpd.tuple2dict(each)
            t = bAssessor.assess(poem_dic, ig_dynasties)
            while (t == (-1, -1, -1)):
                op = raw_input("Network exception. S for skip, enter when fixed")
                if op == 'S':
                    break
                t = bAssessor.assess(poem_dic, ig_dynasties)
            print poem_dic["id"], t
            updates.append((poem_dic["id"], t[0], t[1], t[2]))
        f = open("scores/score" + str(i) + ".txt", "w")
        for each in updates:
            f.write("%d %d %d %d\n" % each)
        f.close()

def main():
    main_scan()

if __name__ == "__main__":
    main()

