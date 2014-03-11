# -*- coding: utf-8 -*-

from __future__ import division
from zpd import ZPD

class CiBaby():

    def __init__(self):

        self.pais = []

        f = open("pai-sim.txt", "r")
        lines = f.readlines()
        for each in lines:
            pai = each.strip()
            self.pais.append(pai)
        f.close()

        f = open("pai-syn.txt", "r")
        lines = f.readlines()
        for each in lines:
            x = each.replace("又名", "、")
            xs = x.split("、")
            for xe in xs:
                pai = xe.strip()
                self.pais.append(pai)

        self.pais = list(set(self.pais))
        print len(self.pais)
        self.pais = [x.decode("utf-8") for x in self.pais]

    def verify(self, subject):
        for each in self.pais:
            if subject.find(each) == 0:
                return True
        return False
    
if __name__ == "__main__":
    zpd = ZPD()
    cb = CiBaby()
    n = zpd.count_all()
    t = open("ci_id_list.txt", "w")
    for i in range(n // 500 + 1):
        print i
        l = i * 500
        r = i * 500 + 500
        poems = zpd.select_by_id(l, r)
        for poem in poems:
            dic = zpd.tuple2dict(poem)
            if cb.verify(dic["subject"]):
                '''
                print dic["subject"]
                print dic["author"]
                print dic["poem"]
                print "=================="
                '''
                t.write(str(dic["id"]) + "\n")
