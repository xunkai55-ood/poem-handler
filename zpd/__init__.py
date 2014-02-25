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

    def pick(self, max_num = 100):

        

