import sqlite3

con = sqlite3.connect("my_data.sqlite")

cur = con.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS test(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT,
            UNIQUE(ID))""")



# cur.execute("""CREATE TABLE IF NOT EXISTS posts(
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             year INTEGER,
#             month INTEGER,
#             data TEXT,
#             UNIQUE(ID)
#             )""")