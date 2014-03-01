'''
Zxk Poem Database
2014.2.25
'''

import sqlite3

class ZPD():

    def __init__(self, path = "_poems.db"):
        'connect to database'

        try:
            self.conn = sqlite3.connect(path)
        except:
            self.conn = None
        
    def count_all(self):
        
        rst = self.conn.execute("SELECT count(*) FROM poems").fetchall()
        return rst[0][0]

    def select_by_id(self, l, r):

        cur = self.conn.cursor()
        rst = cur.execute("SELECT * FROM poems WHERE id > ? AND id <= ? ORDER BY id", (l, r))
        return rst

    def pick_by_id(self, x):

        query = "SELECT * FROM poems WHERE id = ?"
        return self.query(query, (x,))

    def query(self, query, values = None):
        'Use it for query only. Do not use it for updating.'
        
        cur = self.conn.cursor()
        if values == None:
            rst = cur.execute(query).fetchall()
        else:
            rst = cur.execute(query, values).fetchall()
        return rst

    def pick(self, max_num = 100):
        
        cur = self.conn.cursor()
        rst = cur.execute("SELECT * FROM poems ORDER BY RANDOM() LIMIT ?", (max_num,))
        return rst.fetchall()

    def tuple2dict(self, tup):
        dic = {}
        dic["id"] = tup[0]
        dic["dynasty"] = tup[1]
        dic["author"] = tup[2]
        dic["subject"] = tup[3]
        dic["poem"] = tup[4]
        return dic

    def list_dynasties(self):
        query = "SELECT DISTINCT(dynasty) FROM poems"
        return self.query(query)

