import random
import requests
import config
import json
import os
import pprint
from random import randrange
import time
import data_base


class VkAgent:
    def __init__(self, token: str):
        self.token = token


    def get_response(self, url, params):
        return requests.get(url, params=params).json()


    def get_link(self, response, i):

        """Функция запрашивает у VK ссылку на скачивание фото"""

        return response['response']['items'][i]['sizes'][-1]['url']

    def find_users(self, search_params):

        """Функция выполняет поиск пользователей в VK по заданным параметрам и возвращает
               рандомный id пользователя"""

        search_params = search_params
        if len(search_params) < 4:   # На случай, если не придут параметры, будут использованы параметры по умолчанию
            search_params = [1, 1, 25, 'Санкт-Петербург']

        url = 'https://api.vk.com/method/users.search'
        params = {
            'access_token': self.token,
            'v': '5.131',
            'sort': 0,
            'count': 1000,
            'status': search_params[1],
            'sex': search_params[0],
            'age_from': search_params[2],
            'is_closed': False,
            'has_photo': 1,
            'hometown': search_params[3]
        }

        response = self.get_response(url, params)
        list_users = []

        for item in response['response']['items']:
            if not item['is_closed']:
                list_users.append(item['id'])
            else:
                continue

        def select_id_v2(list_users):
            user_id = random.choice(list_users)
            if data_base.record_user(user_id):
                return user_id
            else:
                return select_id_v2(list_users)


        return select_id_v2(list_users)


    def get_photo(self, search_params):

        """Функция запрашиваает id пользователя, и если он удовлетворяет условиям,
         скачивает три самых популярных (на основании лайков и комментариев) фото профиля """

        url = 'https://api.vk.com/method/photos.get'

        user_id = self.find_users(search_params)

        params = {
            'owner_id': user_id,
            'album_id': 'profile',
            'extended': '1',
            'photo_sizes': '1',
            'rev': '1',
            'access_token': self.token,
            'v': '5.131'
        }

        response = self.get_response(url, params)
        time.sleep(0.3)

        """так-как не у всех профилей есть 3 фото и они не проходят проверку, отправляется повторный запрос,
        возможны ситуации, когда бедет много запросов подряд, исмользую sleep дабы не попасть под ограничение
         от VK в не более 3х запросов в секунду"""

        count_photo = len(response['response']['items'])
        if count_photo >= 3:
            photo_dict = {}
            for i in range(count_photo):
                link = self.get_link(response, i)
                likes_count = response['response']['items'][i]['likes']['count']
                comments_count = response['response']['items'][i]['comments']['count']
                photo_dict[likes_count + comments_count] = link
            sorted_dict = sorted(photo_dict.items(), reverse=True)

            list_of_link = []

            for k in range(3):
                list_of_link.append(sorted_dict[k][1])

            count_for_name_photo = 1
            for link in list_of_link:
                f = open(rf'photo\{count_for_name_photo}.jpg', 'wb')
                ufr = requests.get(link)
                f.write(ufr.content)
                f.close()
                count_for_name_photo += 1
            return user_id
        else:
            return self.get_photo(search_params)


    def get_name(self, user_id):
        '''Возвращает имя пользователя VK на основании его ID'''

        url = 'https://api.vk.com/method/users.get'
        params = {
            'access_token': self.token,
            'v': '5.131',
            'user_ids': user_id
        }
        response = self.get_response(url, params)
        return response['response'][0]['first_name']
