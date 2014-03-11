from zpd import ZPD
from zpd import InfluenceDB

def test1():
    'Test the basic usage of ZPD'

    zpd = ZPD()
    arr = zpd.pick(20)
    for each in arr:
        for ele in each:
            print ele
            
def test2():
    "Test the influence tag"

    idb = InfluenceDB()
    zpd = ZPD()
    a = input("num?")
    arr = idb.pick_descend(a)
    cnt = 1
    for each in arr:
        print each
        poem = zpd.tuple2dict(zpd.pick_by_id(each[0]))
        print poem["subject"]
        print poem["author"]
        print poem["poem"]
        print "Rank: " + str(cnt) + " Score: " + str(each[1])
        cnt += 1
        print "========================="

if __name__ == '__main__':
    test2()
