import sqlite3

db_path = "mainBase.sqlite"
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
    con = sqlite3.connect("mainBase.sqlite")
    cur = con.cursor()
    result = cur.execute(f"""SELECT * FROM apps
                        JOIN services ON apps.serviceID=services.id
                         WHERE serviceID = {category_id}""").fetchall()
    return result


def test(category_id):
    con = sqlite3.connect("mainBase.sqlite")
    cur = con.cursor()
    result = cur.execute(f"""SELECT * FROM apps
                             WHERE serviceID = {category_id}""").fetchall()
    return result


def main():
    # tests
    print(get_spec_offers(1))
    print('Done!')


if __name__ == "__main__":
    main()
