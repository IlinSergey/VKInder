import requests
import config
import json
import os
import pprint
from random import randrange


class VkAgent:
    def __init__(self, token: str):
        self.token = token


    def get_response(self, url, params):
        return requests.get(url, params=params).json()


    def get_link(self, response, i=int):
        return response['response']['items'][i]['sizes'][-1]['url']


    def find_users(self):
        url = 'https://api.vk.com/method/users.search'
        params = {
            'access_token': self.token,
            'v': '5.131',
            'sort': 0,
            'count': 1000,
            'status': 6,
            'sex': 1,
            'age_from': 20,
            'is_closed': False,
            'has_photo': 1,
            'fields': ['city']
        }
        response = self.get_response(url, params)
        stop = len(response['response']['items'])
        item = randrange(0, stop)
        id =response['response']['items'][item]['id']
        return id


    def get_photo(self, count: int):
        url = 'https://api.vk.com/method/photos.get'
        id = self.find_users()
        print(id)
        params = {
            'owner_id': id,
            'album_id': 'profile',
            'extended': '1',
            'photo_sizes': '1',
            'rev': '1',
            'access_token': self.token,
            'v': '5.131'
        }

        response = self.get_response(url, params)
        try:
            for i in range(count):
                file_name = response['response']['items'][i]['likes']['count']
                link = self.get_link(response, i)
                f = open(f'backup\{file_name}.jpg', 'wb')
                ufr = requests.get(link)
                f.write(ufr.content)
                f.close()
            print('Фото скачаны')
        except Exception:
            print('Упс, что то пошло не так!')



vk = VkAgent(config.vk_user_token)
vk.get_photo(3)
