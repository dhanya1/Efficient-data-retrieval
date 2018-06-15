import sqlite3
from sqlite3 import Error
#import pandas as pd
import os

class database:
    def __init__(self):
        pass
    def connect(self):
        db_file = os.path.abspath('advertima.db')
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error:
            print(e)

    def execute_query(self,conn,query):
        cur = conn.cursor()
        cur.execute(query)
        result = cur.fetchall()
        return result

if __name__ ==" __main__":
    # This part is just to test the functionality
    db_file = os.path.abspath('advertima.db')
    db = database()
    conn = db.connect(db_file)
    d = db.execute_query(conn,'select * from persons limit 5')
    print(d)
