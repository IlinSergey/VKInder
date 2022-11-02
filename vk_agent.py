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
            'count': 20,
            'status': 4,
            'sex': 1,
            'age_from': 30,
            'is_closed': False,
            'has_photo': 1,
            'hometown': 'Чита'
        }
        response = self.get_response(url, params)
        stop = len(response['response']['items'])
        item = randrange(0, stop)
        id =response['response']['items'][item]['id']
        if not response['response']['items'][item]['is_closed']:
            return id
        else:
            self.find_users()


    def get_photo(self):
        url = 'https://api.vk.com/method/photos.get'
        id = self.find_users()
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
                f = open(f'backup\{id}_{count_for_name_photo}.jpg', 'wb')
                ufr = requests.get(link)
                f.write(ufr.content)
                f.close()
                count_for_name_photo += 1
        else:
            self.get_photo()



vk = VkAgent(config.vk_user_token)
vk.get_photo()
