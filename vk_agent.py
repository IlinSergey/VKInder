import random
from random import randrange
from datetime import date
import time
import json
import os
import shutil

import requests

import config
import data_base


class VkAgent:
    def __init__(self, token: str):
        self.token = token
        self.list_users = []
        self.search_params = []

    def get_response(self, url, params):
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return False

    def get_link(self, response, i):
        """Функция запрашивает у VK ссылку на скачивание фото"""
        return response['response']['items'][i]['sizes'][-1]['url']

    def make_user_list(self, search_params):
        """Создает список id пользователей исходя из параметров поиска"""
        list_users = []
        url_find_user = 'https://api.vk.com/method/users.search'
        params_find_user = {
            'access_token': self.token,
            'v': '5.131',
            'sort': 0,
            'count': 100,
            'status': search_params[1],
            'sex': search_params[0],
            'age_from': search_params[2],
            'is_closed': False,
            'has_photo': 1,
            'hometown': search_params[3]
        }
        response_find_user = self.get_response(url_find_user, params_find_user)
        if response_find_user:
            for item in response_find_user['response']['items']:
                if not item['is_closed']:
                    list_users.append(item['id'])
                else:
                    continue
            self.list_users = list_users

    def select_id(self, list_users, customer_id):
        """Возвращает рандомный id из списка"""
        if len(self.list_users) != 0:
            user_id = random.choice(list_users)
            list_users.remove(user_id)
            if data_base.record_user(user_id, customer_id):
                return user_id
            else:
                return self.select_id(list_users, customer_id)
        else:
            return False
    def get_photo(self, search_params, customer_id):
        """Функция скачивает 3 самых популярных фото пользователя, если фото меньше,
        то скачивает имеющееся количество

         """

        if len(self.list_users) == 0:
            self.make_user_list(search_params)

        url = 'https://api.vk.com/method/photos.get'
        user_id = self.select_id(self.list_users, customer_id)
        if user_id:
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
            if response:
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
                    list_of_link = []
                    for i in range(count_photo):
                        link = self.get_link(response, i)
                        list_of_link.append(link)
                    count_for_name_photo = 1
                    for link in list_of_link:
                        f = open(rf'photo\{count_for_name_photo}.jpg', 'wb')
                        ufr = requests.get(link)
                        f.write(ufr.content)
                        f.close()
                        count_for_name_photo += 1
                    return user_id
            else:
                return False
        else:
            self.make_user_list(search_params)
            return self.get_photo(search_params, customer_id)

    def get_name(self, user_id):
        """Возвращает имя пользователя VK на основании его ID"""
        url = 'https://api.vk.com/method/users.get'
        params = {
            'access_token': self.token,
            'v': '5.131',
            'user_ids': user_id
        }
        response = self.get_response(url, params)
        if response:
            return response['response'][0]['first_name']
        else:
            return False

    def get_default_param(self, user_id):
        """Возвращает информацию о пользователе, необходимую для автоматического поиска пар"""
        url = 'https://api.vk.com/method/users.get'
        params = {
            'access_token': self.token,
            'v': '5.131',
            'user_ids': user_id,
            'fields': 'sex, city, bdate, age'
        }
        response = self.get_response(url, params)
        if response:
            search_params = []
            if response['response'][0]['sex'] == 1:
                search_params.append(2)
            elif response['response'][0]['sex'] == 2:
                search_params.append(1)
            else:
                search_params.append(response['response'][0]['sex'])
            search_params.append(1)  # по умолчанию 'в активном поиске'
            user_bd_year = date.today().strftime("%d/%m/%Y").split('/')  # значение по умолчанию, если возраст скрыт
            try:
                user_bd_year = response['response'][0]['bdate'].split('.')
            except Exception:
                user_bd_year = user_bd_year
            age = date.today().year - int(user_bd_year[2])
            search_params.append(age)
            search_params.append(response['response'][0]['city']['title'])
            return search_params
        else:
            return False

    def clear_dir(self):
        for file in os.listdir('photo'):
            os.remove(f'photo/{file}')

    def clear_search_params(self):
        self.search_params = []
        self.list_users = []
