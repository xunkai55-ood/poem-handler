while True:
    t = raw_input("Paste your cookie here=")
    f = open("__cookies.txt", "w")
    f.write(t)
    f.close()
