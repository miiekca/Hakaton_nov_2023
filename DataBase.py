import sqlite3
class Client:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        self.con = sqlite3.connect(db_path)
        self.cur = self.con.cursor()
    
    def reject_master(self, master_id: int, app_id: int) -> None:
        """Удаление заявки из таблицы offers по id услуги и id мастера. Для отклонения заявки."""
        self.cur.execute(f"""DELETE FROM offers
                    WHERE masterID = {master_id}
                    AND appID = {app_id}""")
        self.con.commit()

    def delete_offers(self, app_id: int) -> None:
        """Удаление всех заявок из таблицы offers по указанному id.
            Статус данной заявки принимает значение True.
            Для приянтия заявки."""
        self.cur.execute(f"""UPDATE apps
                    SET status = 1
                    WHERE id = {app_id}""")
        self.cur.execute(f"""DELETE FROM offers
                    WHERE appID = {app_id}""")
        self.con.commit()

    def reject_user(self, offer_id: int) -> None:
        """Удаление заявки из таблицы offersClientToMaster по указанному id."""
        self.cur.execute(f'''DELETE FROM offersClientToMaster
                    WHERE id = {offer_id}''')
        self.con.commit()
        
    def accept_offer(self, offer_id: int) -> None:
        """Изменение статуса заявки на значение True."""
        self.cur.execute(f"""UPDATE offersClientToMaster
                    SET status = 1
                    WHERE id = {offer_id}""")
        self.con.commit()

    def get_spec_offers(self, category_id: int) -> list:
        """Возвращает список заявок по конкретной категории."""
        result = self.cur.execute(f"""SELECT * FROM apps
                            WHERE serviceID = {category_id}""").fetchall()
        return result

    def city_filter(self, city: str) -> list:
        """Фильтр пользователей по городу."""
        result = self.cur.execute(f'''SELECT * FROM users
                            WHERE city = "{city}"''').fetchall()
        return result

    def get_spec_masters(self, category_id: int) -> list:
        """Фильтр мастеров по предоставляемой услуге."""
        masters = self.cur.execute(f"""SELECT id_master FROM masterService
                            WHERE id_service = {category_id}""").fetchall()
        return masters

    def area_filter(self, area: str) -> list:
        """Фильтр заявок по району."""
        result = self.cur.execute(f"""SELECT * FROM apps
                            WHERE area = '{area}'""").fetchall()
        return result

    def complex_filter(self, area: str = None, city: str = None, priceFrom: int = None, priceTo: int = None, category_id: int = None) -> list:
        """Сложный фильтр, возвращающий список попадающих под него заявок."""
        condition = []
        flag = False
        if area is not None:
            condition.append(f'area = "{area}"')
        if city is not None:
            condition.append(f'city = "{city}"')
            to_join = ' JOIN users u ON u.id = apps.userID'
            flag = True
        if priceFrom is not None:
            condition.append(f'priceFrom >= {priceFrom}')
        if priceTo is not None:
            condition.append(f'priceTo <= {priceTo}')
        if category_id is not None:
            condition.append(f'serviceID = {category_id}')
        if condition:
            request = 'SELECT * FROM apps'
            if flag:
                request += to_join
            request += ' WHERE '
            request +=  " AND ".join(condition)
            print(request)
            result = self.cur.execute(request).fetchall()
            return result
        return condition