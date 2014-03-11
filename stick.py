from zpd import ZPD

if __name__ == "__main__":
    zpd = ZPD()
    while True:
        x = input("id?")
        rst = zpd.pick_by_id(x)
        for each in rst:
            print each
    
