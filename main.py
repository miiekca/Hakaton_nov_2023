from flask import Flask, render_template, session, url_for, redirect, request
import getContent as gt
import helpFunctions as hf
import filterFunctions as fF
from Client import Client
from Client2 import Client2
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)


# Домашняя страница
# Подгружаем мастеров немнога
# Подгружаем категории
# Подгружаем инфу о пользователе
# (готово)
@app.route('/')
def home():
    masters = gt.getMasters()
    if 'user_id' not in session:
        userInfo = 'not login'
    else:
        userInfo = gt.getUserInfo(session['user_id'])[0][1]
    category = gt.getAllCategory()
    # print(masters)
    return render_template('main_singin.html', masters=masters, userInfo=userInfo, categories=category)


# выводим список заявок из категорий, которые принадлежат данному мастеру
@app.route('/masterMode')
def masterMode():
    # вернуть позднее
    # if 'user_id' not in session:
    #     return redirect(url_for('signin'))

    # if gt.checkMaster(session['user_id']):
    #     ## вернуть все категории данного мастера
    #     categories = gt.getAllCategoriesFromId(session['user_id'])
    #     ## список заявок по категориям (список списков)
    #     appList = [hf.get_spec_offers(el) for el in categories]
    #     return render_template('apps.html', content=appList)
    # else:
    #     # здесь редирект на мастер-регистрацию
    #     return 'not content'

    # вернуть юзер id
    # categories = gt.getAllCategoriesFromId(session['user_id'])

    availableServices = gt.getServicesFromMasterID(4)
    # print(availableServices)

    categories = gt.getAllCategoriesFromId(4)
    # print(categories)
    appList = [hf.get_spec_offers(el) for el in categories]
    appList1 = []
    for l1 in appList:
        for tup in l1:
            appList1.append(tup)

    # print(appList)
    # print(appList1)
    return render_template('main_singin_masterMode.html', appList=appList1, availableServices=availableServices)


# Страница заявки (готово) переделать под страницу профиля!!!
@app.route('/appUnit')
def appUnit():
    id = request.args.get('id')
    return render_template('appUnit.html', content=gt.getAppUnit(id))


@app.route('/masterSearchFilter', methods=["POST"])
def masterSearchFilter():
    return 'в разработке'


# Страница списка заявок с приминением фильтра (готово) (возможно работает правильно)
@app.route('/masterFilter', methods=["POST"])
def masterFilter():
    availableServices = gt.getServicesFromMasterID(4)

    client = Client("mainBase.sqlite")
    data = client.complex_filter(request.form.get('area'), request.form.get('city'),
                                 request.form.get('priceFrom'), request.form.get('priceTo'),
                                 request.form.get('serviceID'))
    # Добавить потом
    # if data is None:
    #     return redirect(url_for('masterMode'))
    # print(len(data))
    print(data)
    return render_template('main_singin_masterMode.html', appList=data, availableServices=availableServices)
    # return 'в разработке'


# Результат поиска (готово)
@app.route('/clientSearchFilter', methods=["POST"])
def clientSearchFilter():
    subStr = request.form.get('sub')
    client = Client2("mainBase.sqlite")
    data = client.user_search(subStr)
    if 'user_id' not in session:
        userInfo = 'not login'
    else:
        userInfo = gt.getUserInfo(session['user_id'])[0][1]
    category = gt.getAllCategory()
    print(data)
    return render_template('main_singin.html', masters=data, userInfo=userInfo, categories=category)


# Страница мастеров с применением фильтра (готово)
@app.route('/clientFilter', methods=["POST"])
def clientFilter():
    # клиентский фильтр по мастерам
    client = Client2("mainBase.sqlite")
    data = client.user_filter(request.form.get('city'), request.form.get('serviceID'))
    if data is None:
        redirect(url_for('home'))
    if 'user_id' not in session:
        userInfo = 'not login'
    else:
        userInfo = gt.getUserInfo(session['user_id'])[0][1]
    category = gt.getAllCategory()
    print(data)
    return render_template('main_singin.html', masters=data, userInfo=userInfo, categories=category)


# Заполняем форму заявки
@app.route('/addApp', methods=["POST", "GET"])
def addApp():
    if request.method == 'GET':
        return render_template('addApp.html')
    elif request.method == 'POST':
        serviceID = request.form.get('serviceID')
        content = request.form.get('content')
        area = request.form.get('are')
        priceFrom = request.form.get('priceFrom')
        priceTo = request.form.get('priceTo')
        # передаем все аргументы в функцию валидации

        # при успешной валидации
        # return redirect(url_for('home'))

        # при провальной валидации
        # return redirect(url_for('addApp'))


# переход на страницу мастера
@app.route('/masterPage')
def masterPAge():
    id = request.args.get('id')
    # data = f(id)
    pass


# переход на страницу уведомлений
@app.route('/notification')
def notifications():
    # получить уведомления из БД
    # вернуть список уведомлений

    # у каждого уведомления кнопки принять, отклонить, написать
    pass


# служебная страница для обработки кнопок принять отклонить
@app.route('/acceptReject')
def acceptReject():
    # принятие кнопок принять/отклонить
    pass


# прописать роуты уведомлений мастера

@app.route('/login')
def login():
    # logIn
    username = 42
    session['username'] = username
    return 'залогинься'


# регистрация
@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        if request.form.get('psw'):

            hash = gt.generate_password_hash(request.form.get('psw'))
            res = gt.addUser(request.form.get('name'), request.form.get('phone'), hash)
            if res:
                session['user_id'] = gt.getUserID(request.form.get('phone'))
                return redirect(url_for('home'))
        # else:
        #     print("Неверно заполнены поля", "error")
    return render_template("singup.html", )
    # return redirect(url_for('home'))


# авторизация
@app.route("/signin", methods=["POST", "GET"])
def signin():
    if request.method == "POST":
        res = gt.checkPhoneNumber(request.form.get('phone'))
        print(res)
        if res[0] > 0:
            hash = gt.generate_password_hash(request.form.get('psw'))
            if gt.check_password_hash(hash, request.form.get('psw')):
                session['user_id'] = gt.getUserID(request.form.get('phone'))
                return redirect(url_for('home'))
                # print('успешный вход')
            # else:
            #     print('неверный пароль')
        # else:
        # print('Этот номер не зарегистирован')
    return render_template("singin.html")


# @app.route('/filter', methods=["POST"])
# def filter():
#     id = request.form.get('id')
#     mastersOfCategory = gt.getAllMastersFromCategory(id)
#     mas = gt.getAllMastersFromCategory(id)
#
#     if request.method == 'GET':
#         return render_template('category.html', id=request.args.get('id'))
#     elif request.method == 'POST':
#         arg = request.form.get('id')
#         return render_template('category.html', id=arg)
#     else:
#         return 'empty'


# @app.route('/somePage')
# def somePage():
#     return render_template('somePage.html')


@app.route('/checkLogin')
def checkLogin():
    if 'username' not in session:
        return 'not login'
    else:
        return session['username']


# @app.route('/somePage2')
# def somePage2():
#     return 'somePage2'
#
#
# @app.route('/somePage3')
# def somePage3():
#     return redirect(url_for('somePage2'))


if __name__ == '__main__':
    app.run()
