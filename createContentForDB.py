import sqlite3

con = sqlite3.connect("mainBase.sqlite")


def createApps():
    cur = con.cursor()
    for i in range(40):
        cur.execute(f"""INSERT INTO apps (userID, serviceID, content, status, area, priceFrom, priceTo)
        VALUES ({i}, {i%8}, 'hello world {i}', 0, 'someArea{i%3}', {(i+1) % 5}, {(i+6) % 5})""")
        con.commit()


createApps()

