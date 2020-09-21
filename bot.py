import random
import math
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
from toks import main_token

def random_game(sender, message=''):
  
  start = 'Я загадаю число от 1 до '
  write_message(sender, message)

def write_message(sender, message):
  vk.method('messages.send', {'chat_id': sender, 'message': message, 'random_id': 0})
  print('id: ', sender, 'message: ', message) 

vk = vk_api.VkApi(token=main_token)
longpoll = VkBotLongPoll(vk, group_id=198845838)

listHi = ['здравствуйте', 'привет', 'салам', 'добрый день', 'добро пожаловать', 'хай', 'салам алейкум', 'приветик', 'прив']

for event in longpoll.listen():
  if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat and event.message.get('text') != '':
    reseived_message = event.message.get('text')
    sender = event.chat_id
    print('id: ', sender, 'msg: ', reseived_message)
    if reseived_message.lower() in listHi:
      write_message(sender, random.choice(listHi).title())
    elif reseived_message.lower() == 'rd':
      random_game(sender, message)
    
    

