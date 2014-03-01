from zpd import ZPD

if __name__ == "__main__":
    zpd = ZPD()
    l = zpd.list_dynasties()
    for each in l:
        print each[0]
