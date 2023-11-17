import sqlite3

con = sqlite3.connect("my_data.sqlite")

cur = con.cursor()
result = cur.execute("""SELECT * FROM test""").fetchall()
print(result)


def getRequest():
    con = sqlite3.connect("my_data.sqlite")

    cur = con.cursor()
    result = cur.execute("""SELECT * FROM test""").fetchall()
    return result


def getRequest2(id):
    con = sqlite3.connect("my_data.sqlite")

    cur = con.cursor()
    result = cur.execute(f"""SELECT * FROM test WHERE id={id}""").fetchall()
    return result
