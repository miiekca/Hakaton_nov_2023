import sqlite3
db_path = 'заглушка'
con = sqlite3.connect(db_path)
cur = con.cursor()


def reject_master(master_id: int, app_id: int) -> None:
    """Удаление заявки из таблицы offers по id услуги и id мастера.
    Для отклонения заявки."""
    cur.execute(f"""DELETE FROM offers
                WHERE masterID = {master_id}
                AND appID = {app_id}""")
    con.commit()

def delete_offers(app_id: int) -> None:
    """Удаление всех заявок из таблицы offers по указанному id.
        Статус данной заявки принимает значение True.
        Для приянтия заявки."""
    cur.execute(f"""UPDATE apps
                SET status = 1
                WHERE id = {app_id}""")
    cur.execute(f"""DELETE FROM offers
                WHERE appID = {app_id}""")
    con.commit()

def reject_user(offer_id: int) -> None:
    """Удаление заявки из таблицы offersClientToMaster по указанному id."""
    cur.execute(f'''DELETE FROM offersClientToMaster
                WHERE id = {offer_id}''')
    con.commit()
    
def accept_offer(offer_id: int) -> None:
    """Изменение статуса заявки на значение True."""
    cur.execute(f"""UPDATE offersClientToMaster
                SET status = 1
                WHERE id = {offer_id}""")
    con.commit()

def get_spec_offers(category_id: int) -> list:
    """Возвращает список заявок по конкретной категории."""
    result = cur.execute(f"""SELECT * FROM apps
                         WHERE serviceID = {category_id}""").fetchall()
    return result

def city_filter(city: str) -> list:
    """Фильтр пользователей по городу."""
    result = cur.execute(f'''SELECT * FROM users
                         WHERE city = "{city}"''').fetchall()
    return result

def get_spec_masters(category_id: int) -> list:
    """Фильтр мастеров по предоставляемой услуге."""
    masters = cur.execute(f"""SELECT id_master FROM masterService
                          WHERE id_service = {category_id}""").fetchall()
    return masters

def area_filter(area: str) -> list:
    """Фильтр заявок по району."""
    result = cur.execute(f"""SELECT * FROM apps
                         WHERE area = '{area}'""").fetchall()
    return result

def complex_filter(area: str = None, city: str = None, priceFrom: int = None, priceTo: int = None, category_id: int = None) -> list:
    """Сложный фильтр, возвращающий список попадающих под него заявок."""
    condition = []
    if area is not None:
        condition.append(f'area = "{area}"')
    if city is not None:
        condition.append(f'city = "{city}"')
    if priceFrom is not None:
        condition.append(f'priceFrom >= {priceFrom}')
    if priceTo is not None:
        condition.append(f'priceTo <= {priceTo}')
    if category_id is not None:
        condition.append(f'serviceID = {category_id}')
    if condition:
        request = 'SELECT apps.area, apps.priceFrom, apps.priceTo, apps.serviceID, users.city FROM apps, users WHERE ' + " AND ".join(condition)
        print(request)
    result = cur.execute(request).fetchall()
    return result
    
    

def main():
    #tests
    print('Done!')
    
if __name__ == "__main__":
    main()

