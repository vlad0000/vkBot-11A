import random
import math
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
from toks import main_token, main_group_id

def random_game(peer_id,reseived_message, message):
  lvl = [32, 64, 128, 256]
  num_max = random.choice(lvl)
  # ans = random.randint(1, num_max)
  attempt = int(math.log2(num_max))
  # write_message(peer_id, ('Я загадал абсолютно рандомное число от 1 до ' + str(num_max) + ' \n- твоя задача отгадать какое это число за  ' + str(attempt) + ' попыток' + '\n Я буду лишь подсказывать больше или меньше твое число'))
  
def write_message(peer_id,sender_first_name ,message ):
  vk.method('messages.send', {'peer_id': peer_id, 'message': sender_first_name + ', ' + str(message), 'random_id': 0})
  print('\nbot: ', message) 

def first_name():
  fn = ''
  for user in members['profiles']:
    if user['id'] == from_id:
      fn = user['first_name']
      break
  return fn

def random_user_cool(peer_id):
   user = random.choice(members['profiles'])
   random_user = user['first_name'] + ' ' + user['last_name']
   message = 'счасливчиком является - '+ random_user
   write_message(peer_id, sender_first_name, message)
   
vk = vk_api.VkApi(token = main_token)
longpoll = VkBotLongPoll(vk, group_id = main_group_id)
vk._auth_token()

listHi = ['здравствуйте', 'ку','привет' ,'салам' ,'добрый день' ,'добро пожаловать', 'хай', 'салам алейкум', 'приветик', 'прив']

for event in longpoll.listen():
  if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat and event.message.get('text') != '':
    reseived_message = event.message.get('text')

    from_id = event.message.get('from_id')
    peer_id = event.message.get('peer_id')
    members = vk.method('messages.getConversationMembers', {'peer_id': peer_id, 'fields': 'first_name', 'group_id': main_group_id})
    members_count = members['count']
    sender_first_name = first_name()
    print('\n\npeer_id:', peer_id,'\nfrom_id:', from_id , ' : ', reseived_message)

    
    if reseived_message.lower() in listHi:
      write_message(peer_id, sender_first_name,random.choice(listHi).title())
    elif reseived_message.lower() == 'user_cool':
      random_user_cool(peer_id)