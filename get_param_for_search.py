import pprint
from random import randrange
import config
import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
import json

token = config.vk_group_token

vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)
vk_upload = vk_api.VkUpload(vk)


def write_msg(user_id, message, keyboard=None):
    param = {'user_id': user_id,
             'message': message,
             'random_id': randrange(10 ** 7)}
    if keyboard is not None:
        param['keyboard'] = keyboard.get_keyboard()
    vk.method('messages.send', param)


def get_param_for_search():
    '''Функция опрашивет пользователя для сборов параметров для последующего использования в поиске пользователей VK'''
    params = []

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                request = event.text.lower()

                if request == 'старт':
                    keyboard = VkKeyboard(inline=True)
                    keyboard.add_button('Женщину', color=VkKeyboardColor.NEGATIVE)
                    keyboard.add_button('Мужчину', color=VkKeyboardColor.PRIMARY)
                    write_msg(event.user_id, 'Кого ищем?', keyboard)

                    for event in longpoll.listen():
                        if event.type == VkEventType.MESSAGE_NEW:
                            if event.to_me:
                                request = event.text.lower()
                                if request == 'женщину':
                                    params.append(1)
                                    keyboard = VkKeyboard(inline=True)
                                    keyboard.add_button('Не замужем', color=VkKeyboardColor.SECONDARY)
                                    keyboard.add_button('В поиске', color=VkKeyboardColor.SECONDARY)
                                    keyboard.add_button('Замужем', color=VkKeyboardColor.SECONDARY)
                                    keyboard.add_button('Все сложно', color=VkKeyboardColor.SECONDARY)
                                    write_msg(event.user_id, 'В каком статусе?', keyboard)
                                else:
                                    params.append(2)
                                    keyboard = VkKeyboard(inline=True)
                                    keyboard.add_button('Не женат', color=VkKeyboardColor.SECONDARY)
                                    keyboard.add_button('В поиске', color=VkKeyboardColor.SECONDARY)
                                    keyboard.add_button('Женат', color=VkKeyboardColor.SECONDARY)
                                    keyboard.add_button('Все сложно', color=VkKeyboardColor.SECONDARY)
                                    write_msg(event.user_id, 'В каком статусе?', keyboard)


                                for event in longpoll.listen():
                                    if event.type == VkEventType.MESSAGE_NEW:
                                        if event.to_me:
                                            request = event.text.lower()
                                            if request == 'не женат' or request == 'не замужем':
                                                params.append(1)
                                            elif request == 'в поиске':
                                                params.append(6)
                                            elif request == 'женат' or request == 'замужем':
                                                params.append(4)
                                            elif request == 'все сложно':
                                                params.append(5)

                                            write_msg(event.user_id, 'С какого возраста ищем?')

                                            for event in longpoll.listen():
                                                if event.type == VkEventType.MESSAGE_NEW:
                                                    if event.to_me:
                                                        request = event.text.lower()
                                                        params.append(request)

                                                        write_msg(event.user_id, 'Где ищем (населенный пункт)?')

                                                        for event in longpoll.listen():
                                                            if event.type == VkEventType.MESSAGE_NEW:
                                                                if event.to_me:
                                                                    request = event.text
                                                                    params.append(request)
                                                                    write_msg(event.user_id, 'Готово!')
                                                                    return params





get_param_for_search()