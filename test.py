from zpd import ZPD

def test1():
    'Test the basic usage of ZPD'

    zpd = ZPD()
    arr = zpd.pick(20)
    for each in arr:
        for ele in each:
            print ele

if __name__ == '__main__':
    test1()
