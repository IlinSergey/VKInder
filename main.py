from vk_agent import VkAgent
import config
import os
from random import randrange
from data_base import set_favorite, show_favorite

import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType



token = config.vk_group_token
user_token = config.vk_user_token

vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)
vk_upload = vk_api.VkUpload(vk)

vk_user = VkAgent(config.vk_user_token)



def write_msg(user_id, message, keyboard=None):
    param = {'user_id': user_id,
             'message': message,
             'random_id': randrange(10 ** 7)}
    if keyboard is not None:
        param['keyboard'] = keyboard.get_keyboard()
    vk.method('messages.send', param)


def write_msg_with_photo(user_id):
    resp = vk_upload.photo_messages(photos=['photo/1.jpg', 'photo/2.jpg', 'photo/3.jpg'])
    for ph in resp:
        vk.method('messages.send', {'user_id': user_id, 'attachment': f"photo{ph['owner_id']}_{ph['id']}", 'random_id': randrange(10 ** 7)})


search_params_all_user = {}
current_found_id = None
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            request = event.text.lower()

            if request == 'начать' or request == 'привет':
                write_msg(event.user_id, f'Привет, {vk_user.get_name(event.user_id)}')
                keyboard = VkKeyboard(inline=True)
                keyboard.add_button('Параметры', color=VkKeyboardColor.PRIMARY)
                write_msg(event.user_id, 'Для начала, нужно установить параметры для поиска, позже можно их изменить, отправив команду "Параметры" ', keyboard)

            elif request == 'искать' or request == 'дальше':
                try:
                    id_user = vk_user.get_photo(search_params_all_user[event.user_id])
                    current_found_id = id_user
                    write_msg_with_photo(event.user_id)
                    keyboard = VkKeyboard(inline=True)
                    keyboard.add_button('В избранное', color=VkKeyboardColor.PRIMARY)
                    keyboard.add_button('Дальше', color=VkKeyboardColor.PRIMARY)
                    write_msg(event.user_id, f'{vk_user.get_name(id_user)}  - vk.com/id{id_user}', keyboard)

                except:
                    keyboard = VkKeyboard(inline=True)
                    keyboard.add_button('Параметры', color=VkKeyboardColor.PRIMARY)
                    write_msg(event.user_id, 'Ой-ёй, кажется не установлены параметры для поиска. Нужно это исправить!', keyboard)

            elif request == 'в избранное':
                set_favorite(current_found_id, event.user_id)
                keyboard = VkKeyboard(inline=True)
                keyboard.add_button('Дальше', color=VkKeyboardColor.PRIMARY)
                write_msg(event.user_id, 'Пользователь добавлен в список "Избранные"', keyboard)

            elif request == 'параметры':
                keyboard = VkKeyboard(inline=True)
                keyboard.add_button('Женщину', color=VkKeyboardColor.NEGATIVE)
                keyboard.add_button('Мужчину', color=VkKeyboardColor.PRIMARY)
                write_msg(event.user_id, 'Кого ищем?', keyboard)
                search_params = []

                for event in longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW:
                        if event.to_me:
                            request = event.text.lower()
                            if request == 'женщину':
                                search_params.append(1)
                            else:
                                search_params.append(2)

                            keyboard = VkKeyboard(inline=True)
                            keyboard.add_button('1', color=VkKeyboardColor.SECONDARY)
                            keyboard.add_button('2', color=VkKeyboardColor.SECONDARY)
                            keyboard.add_button('3', color=VkKeyboardColor.SECONDARY)
                            keyboard.add_button('4', color=VkKeyboardColor.SECONDARY)
                            write_msg(event.user_id, 'В каком статусе?')
                            write_msg(event.user_id, 'Не женат (замужем) - 1\nВ активном поиске - 2\nЖенат (Замужем) - 3\nВсе сложно - 4', keyboard)

                            for event in longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW:
                                    if event.to_me:
                                        request = event.text.lower()
                                        if request == '1':
                                            search_params.append(1)
                                        elif request == '2':
                                            search_params.append(6)
                                        elif request == '3':
                                            search_params.append(4)
                                        elif request == '4':
                                            search_params.append(5)
                                        write_msg(event.user_id, 'С какого возраста ищем?')

                                        for event in longpoll.listen():
                                            if event.type == VkEventType.MESSAGE_NEW:
                                                if event.to_me:
                                                    request = event.text.lower()
                                                    search_params.append(request)
                                                    write_msg(event.user_id, 'Где ищем (населенный пункт)?')

                                                    for event in longpoll.listen():
                                                        if event.type == VkEventType.MESSAGE_NEW:
                                                            if event.to_me:
                                                                request = event.text
                                                                search_params.append(request)
                                                                search_params_all_user[event.user_id] = search_params
                                                                write_msg(event.user_id, 'Готово, параметры сохранены!')
                                                                keyboard = VkKeyboard(inline=True)
                                                                keyboard.add_button('Искать', color=VkKeyboardColor.PRIMARY)
                                                                write_msg(event.user_id, 'Теперь можно искать пару!', keyboard)
                                                                break
                                                    break
                                        break
                            break
            elif request == 'избранное':
                user_list = show_favorite(event.user_id)
                if len(user_list) < 1:
                    keyboard = VkKeyboard(inline=True)
                    keyboard.add_button('Искать', color=VkKeyboardColor.PRIMARY)
                    write_msg(event.user_id, 'Список "Избранное" пуст!\nДавай поскорее найдем кого-нибудь', keyboard)
                else:
                    for user in user_list:
                        write_msg(event.user_id,f'{vk_user.get_name(user)}  - vk.com/id{user}')
            elif request == 'пока':
                write_msg(event.user_id, 'Пока((')
            elif request == 'помощь' or request == 'help' or request == 'хелп':
                write_msg(event.user_id, 'Комманды для бота:\n"Параметры" - установить параметры поиска.\n"Искать" - искать пару.\n"Избранное" - показать список избранных пользователей')
            else:
                write_msg(event.user_id, 'Не понял вашего ответа...')
