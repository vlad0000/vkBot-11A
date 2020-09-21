import random
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from toks import main_token

def write_message(sender, message):
  vk.method('messages.send', {'user_id': sender, 'message': message, 'random_id': 0})
  print('id: ', sender, 'message: ', message) 

vk = vk_api.VkApi(token=main_token)
longpoll = VkLongPoll(vk)
listHi = ['здравствуйте', 'привет', 'салам', 'добрый день', 'добро пожаловать', 'хай', 'салам алейкум', 'приветик', 'прив']


for event in longpoll.listen():
  if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
    reseived_message = event.text
    sender = event.user_id
    if reseived_message.lower() in listHi:
      write_message(sender, random.choice(listHi).title())
    else:
      write_message(sender, 'Я еще не научен понимать такие команды &#128553;&#128553;&#128553;')

