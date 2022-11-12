import pprint
import os
from random import randrange
import config
import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType



from vk_agent import VkAgent

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

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            request = event.text.lower()

            if request == "привет":
                write_msg(event.user_id, f"Привет, {event.user_id}")
            elif request == "пока":
                write_msg(event.user_id, "Пока((")
            elif request == 'поехали':
                write_msg(event.user_id, f'Ля vk.com/id{vk_user.get_photo(search_params_all_user[event.user_id])}')
                write_msg_with_photo(event.user_id)
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
                                keyboard = VkKeyboard(inline=True)
                                keyboard.add_button('Не замужем', color=VkKeyboardColor.SECONDARY)
                                keyboard.add_button('В поиске', color=VkKeyboardColor.SECONDARY)
                                keyboard.add_button('Замужем', color=VkKeyboardColor.SECONDARY)
                                keyboard.add_button('Все сложно', color=VkKeyboardColor.SECONDARY)
                                write_msg(event.user_id, 'В каком статусе?', keyboard)
                            else:
                                search_params.append(2)
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
                                            search_params.append(1)
                                        elif request == 'в поиске':
                                            search_params.append(6)
                                        elif request == 'женат' or request == 'замужем':
                                            search_params.append(4)
                                        elif request == 'все сложно':
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
                                                                write_msg(event.user_id, 'Готово, параметры сохранены!')
                                                                search_params_all_user[event.user_id] = search_params
                                                                break
                                                    break
                                        break
                            break
            else:
                write_msg(event.user_id, "Не понял вашего ответа...")
