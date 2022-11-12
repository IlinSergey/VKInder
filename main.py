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




for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:
            request = event.text.lower()

            if request == "привет":
                write_msg(event.user_id, f"Хай, {event.user_id}")
            elif request == "пока":
                write_msg(event.user_id, "Пока((")
            elif request == 'поехали':
                write_msg(event.user_id, f'Ля vk.com/id{vk_user.get_photo()}')
                write_msg_with_photo(event.user_id)
            else:
                write_msg(event.user_id, "Не поняла вашего ответа...")
