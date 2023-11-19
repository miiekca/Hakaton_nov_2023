import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

con = sqlite3.connect("mainBase.sqlite")


def getMasters():
    con = sqlite3.connect("mainBase.sqlite")

    cur = con.cursor()
    result = cur.execute("""SELECT DISTINCT users.id, users.fullName, users.city,
                        users.content, services.content FROM users 
                        JOIN masterService ON users.id=masterService.id_master 
                        JOIN services ON masterService.id_service = services.id
                        WHERE isMaster = 1 GROUP BY users.id LIMIT 5""").fetchall()
    return result


def getUserInfo(id):
    con = sqlite3.connect("mainBase.sqlite")

    cur = con.cursor()
    result = cur.execute(f"""SELECT * FROM users WHERE id={id}""").fetchall()
    return result


def getAllCategory():
    con = sqlite3.connect("mainBase.sqlite")

    cur = con.cursor()
    result = cur.execute(f"""SELECT * FROM services""").fetchall()
    return result


def getAllMastersFromCategory(categoryID):
    con = sqlite3.connect("mainBase.sqlite")

    cur = con.cursor()
    result = cur.execute(f"""SELECT * FROM users WHERE id=(SELECT )""").fetchall()
    return result


def validationAppForm(serviceID, content, area, priceFrom, priceTo):
    if serviceID is None or content is None or area is None or priceFrom is None or priceTo is None:
        return False


def getUser(id):
    con = sqlite3.connect("mainBase.sqlite")

    cur = con.cursor()
    result = cur.execute(f"""SELECT * FROM users WHERE id={id}""").fetchall()
    return result


def checkMaster(id):
    con = sqlite3.connect("mainBase.sqlite")

    cur = con.cursor()
    result = cur.execute(f"""SELECT * FROM users WHERE id={id}""").fetchall()
    return result[0][6]


def getAllCategoriesFromId(id):
    con = sqlite3.connect("mainBase.sqlite")

    cur = con.cursor()
    result = cur.execute(f"""SELECT * FROM masterService WHERE id_master={id}""").fetchall()
    return [el[1] for el in result]


def getAppUnit(id):
    if id == None:
        return None
    con = sqlite3.connect("mainBase.sqlite")

    cur = con.cursor()
    result = cur.execute(f"""SELECT * FROM apps WHERE id={id}""").fetchall()
    return result[0]


def addUser(name, phone, hpsw):
    con = sqlite3.connect("mainBase.sqlite")
    cur = con.cursor()
    try:
        cur.execute(f"SELECT COUNT(*) as `count` FROM users WHERE phoneNumber LIKE '{phone}'")
        res = cur.fetchone()
        if res[0] > 0:
            print("Пользователь с таким номером уже существует")
            return False

        cur.execute("INSERT INTO users (fullName, password, phoneNumber) VALUES(?, ?, ?)", (name, hpsw, phone))
        con.commit()
        return True
    except sqlite3.Error as e:
        print("Ошибка добавления пользователя в БД " + str(e))
        return False


def getUserID(phone):
    con = sqlite3.connect("mainBase.sqlite")

    cur = con.cursor()
    result = cur.execute(f"""SELECT id FROM users WHERE phoneNumber='{phone}'""").fetchall()
    return result[0][0]


def checkPhoneNumber(phone):
    con = sqlite3.connect("mainBase.sqlite")

    cur = con.cursor()
    cur.execute(f"SELECT COUNT(*) as `count` FROM users WHERE phoneNumber LIKE '{phone}'")
    return cur.fetchone()


def getServicesFromMasterID(id):
    con = sqlite3.connect("mainBase.sqlite")

    cur = con.cursor()
    cur.execute(f"""SELECT services.id, services.content FROM services
                JOIN masterService ON services.id = masterService.id_service
                WHERE masterService.id_master={id}""")
    return cur.fetchall()


def getEmpty():
    return 1


if __name__ == '__main__':
    checkMaster(2)
