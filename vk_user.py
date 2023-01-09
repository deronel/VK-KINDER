import requests
from datetime import datetime
from funck_for_BD import users_insert, pretendents_insert
import operator
from pprint import pprint


class VK:
    def __init__(self, access_token, version='5.131'):
        self.token = access_token
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}


    def search_people(self, city, bdate, sex):
        '''Метод для поиска претендентов в Вк. На вход принимает название города, год рождения, пол.
         Вызывает метод поиска фотографий - download_from_vk. Вызывает функцию,
         которая вносит собранную информацию  (id-претендента, имя, фамили, 3 фотографии) в БД.'''
        link_profile = 'https://vk.com/id'
        URL = 'https://api.vk.com/method/users.search'
        params = {
            'count': 100,
            'sex': sex,
            'hometown': city,
            'birth_year': bdate[-4:],  # Берем год  (считаем с конца)
            'fields': 'photo_200',
            'is_closed': 0,
            'has_photo': 1,
            'v': '5.131'
        }
        response = requests.get(URL, params={**self.params, **params}).json()

        for element in response['response']['items']:
            list_photo = self.download_from_vk(element['id'])

            try:
                photo1 = list_photo[0][0]
            except:  # Тут надо посмотреть какой код ошибки формируется
                photo1 = 'К сожалению фото №1 нет'
            try:
                photo2 = list_photo[1][0]
            except:  # Тут надо посмотреть какой код ошибки формируется
                photo2 = 'К сожалению фото №2 нет'
            try:
                photo3 = list_photo[2][0]
            except:  # Тут надо посмотреть какой код ошибки формируется
                photo3 = 'К сожалению фото №3 нет'

            pretendents_insert(self.id, element['id'], element['first_name'], element['last_name'], photo1, photo2,
                               photo3)


    def users_info(self, user_id):
        '''Метод для  получения информации о пользователе. На вход принимает id пользователя Вк.
        Вызывает метод поиска людей -  search_people. Возвращает имя пользователя.'''
        url = 'https://api.vk.com/method/users.get'
        params = {'user_ids': user_id,
                  'fields': 'sex, bdate, city',
                  'v': '5.131'
                  }
        response = requests.get(url, params={**self.params, **params})
        self.id = response.json()['response'][0]['id']
        users_insert(self.id, response.json()['response'][0]['first_name'], response.json()['response'][0]['last_name'],
                     response.json()['response'][0]['city']['title'], response.json()['response'][0]['bdate'][-4:],
                     response.json()['response'][0]['sex'])
        if response.json()['response'][0]['sex'] == 1:
            sex = 2
        else:
            sex = 1
        self.search_people(response.json()['response'][0]['city']['title'], response.json()['response'][0]['bdate'],
                           sex)

        return response.json()['response'][0]['first_name']


    def download_from_vk(self, user_id):
        '''Метод для поиска фотографий. На вход принимает id-претендента. Возвращает отсортированный кортеж,
        где первый элемент – ссылка на фото, второй – кол-во лайков. '''
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': user_id, 'album_id': 'profile', 'extended': 1, 'count': 100}
        try:  # Блок try нужен чтобы код не падал, когда приходит id закрытого профиля
            response = requests.get(url, params={**self.params, **params})
            dict_likes = {}

            for i in range(10):
                try:  # Блок try нужен чтобы пройти все индексы
                    len_sizes = len(response.json()['response']['items'][i][
                                        'sizes'])  # Считаю длину Sizes чтобы взять фото в макс. качестве
                    dict_likes[response.json()['response']['items'][i]['sizes'][len_sizes - 1]['url']] = \
                    response.json()['response']['items'][i]['likes']['count']
                except IndexError:
                    pass

            sorted_tuple = sorted(dict_likes.items(), key=operator.itemgetter(1))

            return sorted_tuple
        except KeyError:
            pass


