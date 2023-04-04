from config import USER_TOKEN, COMM_TOKEN
import vk_api
import requests
import datetime
from vk_api.longpoll import VkLongPoll, VkEventType
from random import randrange
from database import select, insert_data_users, insert_data_seen_users


class VKBot:
    def __init__(self):
        print('Bot was created')
        self.vk = vk_api.VkApi(token=comm_token)  # АВТОРИЗАЦИЯ СООБЩЕСТВА
        self.longpoll = VkLongPoll(self.vk)  # РАБОТА С СООБЩЕНИЯМИ

    def write_msg(self, user_id, message):
        """МЕТОД ДЛЯ ОТПРАВКИ СООБЩЕНИЙ"""
        self.vk.method('messages.send', {'user_id': user_id,
                                         'message': message,
                                         'random_id': randrange(10 ** 7)})

    def get_user_name(self, user_id):
        """ПОЛУЧЕНИЕ ИМЕНИ ПОЛЬЗОВАТЕЛЯ, КОТОРЫЙ НАПИСАЛ БОТУ"""
        url = f'https://api.vk.com/method/users.get'
        params = {'access_token': user_token,
                  'user_ids': user_id,
                  'v': '5.131'}
        repl = requests.get(url, params=params)
        response = repl.json()
        try:
            information_dict = response['response']
            for user in information_dict:
                for key, value in user.items():
                    first_name = user.get('first_name')
                    return first_name
        except KeyError:
            self.write_msg(user_id, 'Ошибка получения токена, введите токен в переменную - user_token')

    def get_sex(self, user_id):
        """ПОЛУЧЕНИЕ ПОЛА ПОЛЬЗОВАТЕЛЯ, МЕНЯЕТ НА ПРОТИВОПОЛОЖНЫЙ"""
        url = f'https://api.vk.com/method/users.get'
        params = {'access_token': user_token,
                  'user_ids': user_id,
                  'fields': 'sex',
                  'v': '5.131'}
        repl = requests.get(url, params=params)
        response = repl.json()
        try:
            information_list = response['response']
            for user in information_list:
                if user.get('sex') == 2:
                    find_sex = 1
                    return find_sex
                elif user.get('sex') == 1:
                    find_sex = 2
                    return find_sex
        except KeyError:
            self.write_msg(user_id, 'Ошибка получения токена, введите токен в переменную - user_token')

    def get_age_low(self, user_id):
        """ПОЛУЧЕНИЕ ВОЗРАСТА ПОЛЬЗОВАТЕЛЯ ИЛИ НИЖНЕЙ ГРАНИЦЫ ДЛЯ ПОИСКА"""
        url = url = f'https://api.vk.com/method/users.get'
        params = {'access_token': user_token,
                  'user_ids': user_id,
                  'fields': 'bdate',
                  'v': '5.131'}
        repl = requests.get(url, params=params)
        response = repl.json()
        try:
            information_list = response['response']
            for user in information_list:
                date = user.get('bdate')
            date_list = date.split('.')
            if len(date_list) == 3:
                year = int(date_list[2])
                year_now = int(datetime.date.today().year)
                return year_now - year
            elif len(date_list) == 2 or date not in information_list:
                self.write_msg(user_id, 'Введите нижний порог возраста (min - 16): ')
                for event in self.longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                        age = event.text
                        return age
        except KeyError:
            self.write_msg(user_id, 'Ошибка получения токена')


    def get_age_high(self, user_id):
        """ПОЛУЧЕНИЕ ВОЗРАСТА ПОЛЬЗОВАТЕЛЯ ИЛИ ВЕРХНЕЙ ГРАНИЦЫ ДЛЯ ПОИСКА"""
        url = url = f'https://api.vk.com/method/users.get'
        params = {'access_token': user_token,
                  'user_ids': user_id,
                  'fields': 'bdate',
                  'v': '5.131'}
        repl = requests.get(url, params=params)
        response = repl.json()
        try:
            information_list = response['response']
            for user in information_list:
                date = user.get('bdate')
            date_list = date.split('.')
            if len(date_list) == 3:
                year = int(date_list[2])
                year_now = int(datetime.date.today().year)
                return year_now - year
            elif len(date_list) == 2 or date not in information_list:
                self.write_msg(user_id, 'Введите верхний порог возраста (max - 65): ')
                for event in self.longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                        age = event.text
                        return age
        except KeyError:
            self.write_msg(user_id, 'Ошибка получения токена, введите токен в переменную - user_token')

    def cities(self, user_id, city_name):
        """ПОЛУЧЕНИЕ ID ГОРОДА ПОЛЬЗОВАТЕЛЯ ПО НАЗВАНИЮ"""
        url = url = f'https://api.vk.com/method/database.getCities'
        params = {'access_token': user_token,
                  'country_id': 1,
                  'q': f'{city_name}',
                  'need_all': 0,
                  'count': 1000,
                  'v': '5.131'}
        repl = requests.get(url, params=params)
        response = repl.json()
        try:
            information_list = response['response']
            city_list = information_list['items']
            for user in city_list:
                found_city_name = user.get('title')
                if found_city_name == city_name:
                    found_city_id = user.get('id')
                    return int(found_city_id)
        except KeyError:
            self.write_msg(user_id, 'Ошибка получения токена')

    def find_city(self, user_id):
        """ПОЛУЧЕНИЕ ИНФОРМАЦИИ О ГОРОДЕ ПОЛЬЗОВАТЕЛЯ"""
        url = f'https://api.vk.com/method/users.get'
        params = {'access_token': user_token,
                  'fields': 'city',
                  'user_ids': user_id,
                  'v': '5.131'}
        repl = requests.get(url, params=params)
        response = repl.json()
        try:
            information_dict = response['response']
            for user in information_dict:
                if 'city' in user:
                    city = user.get('city')
                    id = str(city.get('id'))
                    return id
                elif 'city' not in user:
                    self.write_msg(user_id, 'Введите название вашего города: ')
                    for event in self.longpoll.listen():
                        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                            city_name = event.text
                            id_city = self.cities(user_id, city_name)
                            if id_city != '' or id_city != None:
                                return str(id_city)
                            else:
                                break
        except KeyError:
            self.write_msg(user_id, 'Ошибка получения токена')

    def find_user(self, user_id):
        """ПОИСК ЧЕЛОВЕКА ПО ПОЛУЧЕННЫМ ДАННЫМ"""
        url = f'https://api.vk.com/method/users.search'
        params = {'access_token': user_token,
                  'v': '5.131',
                  'sex': self.get_sex(user_id),
                  'age_from': self.get_age_low(user_id),
                  'age_to': self.get_age_high(user_id),
                  'city': self.find_city(user_id),
                  'fields': 'is_closed, id, first_name, last_name',
                  'status': '1' or '6',
                  'count': 500}
        resp = requests.get(url, params=params)
        resp_json = resp.json()
        try:
            response_data = resp_json['response']
            person_list = response_data['items']
            for person in person_list:
                if person.get('is_closed') == False:
                    first_name = person.get('first_name')
                    last_name = person.get('last_name')
                    vk_id = str(person.get('id'))
                    insert_data_users(first_name, last_name, vk_id)
                else:
                    continue
            return f'Поиск завершён'
        except KeyError:
            self.write_msg(user_id, 'Ошибка получения токена')

    def get_photos_id(self, user_id):
        """ПОЛУЧИТЬ ФОТО ID ПО ПОПУЛЯРНОСТИ"""
        url = 'https://api.vk.com/method/photos.getAll'
        params = {'access_token': user_token,
                  'type': 'album',
                  'owner_id': user_id,
                  'extended': 1,
                  'count': 25,
                  'v': '5.131'}
        resp = requests.get(url, params=params)
        resp_json = resp.json()
        try:
            person_list = resp_json['response']['items']
            photo_list = {i.get('likes').get('count'): str(i.get('id')) for i in person_list if i.get('likes').get('count')}
            return sorted(photo_list.items(), reverse=True)
        except KeyError:
            self.write_msg(user_id, 'Ошибка получения токена')

    def get_photo(self, user_id, num):
        """ПОЛУЧИТЬ ФОТО ID"""
        photo_list = self.get_photos_id(user_id)
        if num <= len(photo_list):
            return photo_list[num - 1][1]

    def send_photo(self, user_id, message, offset, num):
        """ОТПРАВИТЬ ФОТО"""
        photo_id = self.get_photo(self.person_id(offset), num)
        if photo_id:
            self.vk.method('messages.send', {'user_id': user_id,
                                             'access_token': user_token,
                                             'message': message,
                                             'attachment': f'photo{self.person_id(offset)}_{photo_id}',
                                             'random_id': 0})

    def find_persons(self, user_id, offset):
        self.write_msg(user_id, self.found_person_info(offset))
        self.person_id(offset)
        insert_data_seen_users(self.person_id(offset), offset)
        self.send_photo(user_id, 'Фото 1', offset, 1)
        self.send_photo(user_id, 'Фото 2', offset, 2)
        self.send_photo(user_id, 'Фото 3', offset, 3)

    def found_person_info(self, offset):
        """ВЫВОД ИНФОРМАЦИИ О НАЙДЕННОМ ПОЛЬЗОВАТЕЛИ"""
        tuple_person = select(offset)
        person_list = []
        for i in tuple_person:
            person_list.append(i)
        return f'{person_list[0]} {person_list[1]}, ссылка - {person_list[3]}'

    def person_id(self, offset):
        """ВЫВОД ID НАЙДЕННОГО ПОЛЬЗОВАТЕЛЯ"""
        tuple_person = select(offset)
        person_list = []
        for i in tuple_person:
            person_list.append(i)
        return str(person_list[2])


bot = VKBot()
