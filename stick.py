from zpd import ZPD

if __name__ == "__main__":
    zpd = ZPD()
    while True:
        x = input("id?")
        rst = zpd.pick_by_id(x)
        if len(rst) == 0:
            print "invalid id"
        else:
            for each in rst[0]:
                print each
    
