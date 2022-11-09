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

    def find_users(self):

        """Функция выполняет поиск пользователей в VK по заданным параметрам и возвращает
        рандомный id пользователя"""

        url = 'https://api.vk.com/method/users.search'
        params = {
            'access_token': self.token,
            'v': '5.131',
            'sort': 0,
            'count': 1000,
            'status': 6,
            'sex': 1,
            'age_from': 25,
            'is_closed': False,
            'has_photo': 1,
            'hometown': 'Москва'
        }

        response = self.get_response(url, params)

        def select_id_v2(response):
            list_users = []
            for item in response['response']['items']:
                list_users.append(item['id'])
            return random.choice(list_users)


        def select_id(response):
            response_select_id = response
            stop = len(response_select_id['response']['items'])
            item = randrange(1, stop)
            id_us = response_select_id['response']['items'][item]['id']
            is_closed = response_select_id['response']['items'][item]['is_closed']

            if not is_closed:
                return id_us
            else:
                select_id(response)

        user_id = select_id_v2(response)
        print(user_id)
        if user_id is None:
            select_id(response)
        else:
            if data_base.record_user(user_id):
                print(user_id)
                return user_id
            else:
                select_id(response)

    def get_photo(self):

        """Функция запрашиваает id пользователя, и если он удовлетворяет условиям,
         скачивает три самых популярных (на основании лайков и комментариев) фото профиля """

        url = 'https://api.vk.com/method/photos.get'

        user_id = self.find_users()
        if user_id is None:
            self.find_users()

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
            count_for_name_photo = 1
            photo_dict = {}
            for i in range(count_photo):
                link = self.get_link(response, i)
                count_for_name_photo += 1
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
            self.get_photo()





vk = VkAgent(config.vk_user_token)
vk.get_photo()
