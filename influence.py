#######################################
# influence.py
# This code is aimed to assess each poem an influence value.
#######################################

from zpd import ZPD
from functions import is_chinese

class Assessor():
    'Abstract class of assessors.'
    
    def assess(poem):
        return 0

class BaiduAssessor(Assessor):
    'Assessor using a search-based method.'

    def to_query_style(self, u_str, minchar = 10, maxchar = 12):
        rst = u""
        cnt = 0
        for each in u_str:
            if cnt == maxchar:
                break
            elif is_chinese(each):
                rst += each
                cnt += 1
            elif cnt < minchar:
                rst += u" "
            else:
                break
        return rst

    def assess(self, poem_dic):
        subject = poem_dic["subject"]
        poem = poem_dic["poem"]
        query_str = self.to_query_style(subject, 2) + u' ' + self.to_query_style(poem, 5, 20)
        print query_str

def main():
    zpd = ZPD()
    bAssessor = BaiduAssessor()
    while True:
        poem_tup = zpd.pick(1)[0]
        poem_dic = zpd.tuple2dict(poem_tup)
        bAssessor.assess(poem_dic)
        if raw_input("stop? S") == 'S':
            break


if __name__ == "__main__":
    main()

