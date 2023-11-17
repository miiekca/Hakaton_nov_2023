import sqlite3

con = sqlite3.connect("my_data.sqlite")

cur = con.cursor()
# cur.execute("""INSERT INTO test (content) VALUES ('goodbye World')""")
cur.execute("""INSERT INTO test (content) VALUES ('Lets GOOOO')""")
con.commit()