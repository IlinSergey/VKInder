from random import randrange
import config
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_agent import VkAgent

token = config.vk_group_token

vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)

vk_photo = VkAgent(config.vk_user_token)



def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7),})


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:
            request = event.text

            if request == "привет":
                write_msg(event.user_id, f"Хай, {event.user_id}")
            elif request == "пока":
                write_msg(event.user_id, "Пока((")
            elif request == 'Поехали':
                link = vk_photo.get_photo()
                list_photo = ['backup\\1.jpg']
                write_msg(event.user_id, f'Ля vk.com/id{link}')
            else:
                write_msg(event.user_id, "Не поняла вашего ответа...")