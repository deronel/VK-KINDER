import sqlalchemy
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from models import create_tables,USERS,PRETENDENTS,FAVOURITES
from pprint import pprint
from key_bd import user_login, user_key, name_bd


DSN = f'postgresql://{user_login}:{user_key}@localhost:5432/{name_bd}' # Строка подключения к базе данных
engine = sqlalchemy.create_engine(DSN)

# create_tables(engine) # Эта функция создает/пересоздает таблицы. Для создания необходимо раскомментировать, потом закомментировать. Иначе таблицы будут пересоздаваться каждый раз.

Session = sessionmaker(bind=engine)
session = Session()


def users_insert(id_vk: int, first_name: str, last_name: str, city: str, dbirth: int, sex: int):
    '''Функция сначала проверяет есть ли в таблице USERS пользователь, которого вы собираетесь внести. Если такого пользователя нет, то вносит
     в таблицу USERS поля: id_vk-пользователя, фамилию, имя, город, возраст, пол. id_vk всегда уникальны.
    '''
    list_id_vk = []
    for users in session.query(USERS).all():
        list_id_vk.append(users.id_vk)
    if id_vk not in list_id_vk:
        values_ = USERS(id_vk = id_vk, first_name = first_name, last_name = last_name, city = city, dbirth = dbirth, sex = sex)
        session.add(values_)
        session.commit()
        return f'Пользователь с id:{id_vk} добавлен в БД'
    else:
        return f'Пользователь с id:{id_vk} уже есть в БД'


def pretendents_insert(id_vk: int, id_vk_pret: int, first_name: str, last_name: str,  photo_1: str, photo_2: str, photo_3: str):
    '''
    Сначала функция проверяет есть ли в таблице PRETENDENTS id_vk текущего претендента.
    Если нет то заносит в таблицу PRETENDENTS поля: id_user (это поле id из таблицы USERS), id_vk_pret, фамилию, имя, ссылки на фото.
    '''
    list_id_vk_pret = []
    for users in session.query(USERS).filter(USERS.id_vk == id_vk): # Находим id пользователя
        id_user = users.id
    for pretendents in session.query(PRETENDENTS).filter(PRETENDENTS.id_user == id_user): # По этому id пользователя в таблице PRETENDENTS находим id_vk претендента и помещаем их в список
        list_id_vk_pret.append(pretendents.id_vk_pret)
    if id_vk_pret not in list_id_vk_pret: # Если id_vk претендента нет в списке (а значит и в таблице тоже нет) то добавляем новую запись
        values_ = PRETENDENTS(id_user = id_user, id_vk_pret = id_vk_pret, first_name = first_name, last_name = last_name, photo_1 = photo_1, photo_2 = photo_2, photo_3 = photo_3)
        session.add(values_)
        session.commit()
        return f'Претендент с id:{id_vk_pret} добавлен в БД'
    else:
        return f'Претендент с id:{id_vk_pret} уже есть в БД'


def favourites_insert(id_vk: int, id_vk_fav: int, first_name: str, last_name: str,  photo_1: str, photo_2: str, photo_3: str):
    '''
    Сначала функция по id_vk находит в таблице USERS id пользователя (это нужно чтобы связать пользователя и избранного), затем
    вставляет в таблицу FAVOURITES поля: id_user (это поле id из таблицы USERS), id_vk_fav, фамилию, имя, ссылки на фото.
    '''
    list_id_vk_fav = []
    for users in session.query(USERS).filter(USERS.id_vk == id_vk): # Находим id пользователя
        id_user = users.id
    for favourites in session.query(FAVOURITES).filter(FAVOURITES.id_user == id_user): # По этому id пользователя в таблице FAVOURITES находим id_vk избранного и помещаем их в список
        list_id_vk_fav.append(favourites.id_vk_fav)
    if id_vk_fav not in list_id_vk_fav:  # Если id_vk избранного нет в списке (а значит и в таблице тоже нет) то добавляем новую запись
        values_ = FAVOURITES(id_user = id_user, id_vk_fav = id_vk_fav, first_name = first_name, last_name = last_name, photo_1 = photo_1, photo_2 = photo_2, photo_3 = photo_3)
        session.add(values_)
        session.commit()
        return f'Избранный с id:{id_vk_fav} добавлен в БД'
    else:
        return f'Избранный с id:{id_vk_fav} уже есть в БД'


def pretendents_output(id_vk: int):
    '''Функция на вход принимает id_vk пользователя. Функция возращает список списков, где 0,1,2,3,4,5 элементы вложенного списка это id_vk претендента, имя, фамилия
     и ссылки на фото соответственно.'''
    pretendents_ = []
    for pretendents in session.query(PRETENDENTS).join(USERS).filter(USERS.id_vk == id_vk).all():
        list_= [pretendents.id_vk_pret, pretendents.first_name, pretendents.last_name, pretendents.photo_1, pretendents.photo_2, pretendents.photo_3]
        pretendents_.append(list_)
    return pretendents_


def favourites_output(id_vk: int):
    '''Функция на вход принимает id_vk пользователя. Функция возращает список списков, где 0,1,2,3,4,5 элементы вложенного списка это id_vk избранного, имя, фамилия
     и ссылки на фото соответственно.'''
    favourites_ = []
    for favourite in session.query(FAVOURITES).join(USERS).filter(USERS.id_vk == id_vk).all():
        list_ = [favourite.id_vk_fav, favourite.first_name, favourite.last_name, favourite.photo_1, favourite.photo_2, favourite.photo_3]
        favourites_.append(list_)
    return favourites_


def vk_users_param_output(id_vk: int):
    '''Функция на вход принимает id_vk пользователя. Функция возращает город,возраст, пол пользователя.
    Не знаю, нужна ли эта функция вообще...Может пригодиться когда делается запрос по параметрам'''
    for users in session.query(USERS).filter(USERS.id_vk == id_vk):
        return users.city,users.dbirth,users.sex


def delete_user(id_vk: int):
    '''Функция на вход принимает id_vk пользователя. Функция удаляет из таблиц всех претендентов пользователя, избранных пользователя
    и самого пользователя'''
    try:
        for  user in session.query(USERS).filter(USERS.id_vk == id_vk).all():
            id_user = user.id
        session.query(PRETENDENTS).filter(PRETENDENTS.id_user ==id_user).delete()
        session.query(FAVOURITES).filter(FAVOURITES.id_user == id_user).delete()
        session.query(USERS).filter(USERS.id_vk == id_vk).delete()
        session.commit()
        return f'Пользователь с id:{id_vk} удален из БД'
    except UnboundLocalError:
        return f'в БД пользователя с id:{id_vk} нет'
session.close()

