from food import Hamburger, Chips, Drink
from utils import ORDER, PICKUP

def choose_food_class(food_dict):
   food_class_list = []

   for food in food_dict:
      if food == 'hamburger':
         food_class_list.append(Hamburger(food_dict[food]))
      elif food == 'fries':
         food_class_list.append(Chips(food_dict[food]))
      elif food == 'drink':
         food_class_list.append(Drink(food_dict[food]))

   if len(food_class_list) == 0:
      return food_dict
   return food_class_list

def adaptor(message_received, addr):
   new_message = {
      'method': None,
      'args': {
         'food': None,
         'address': None
      }
   }
   if message_received['method'] == 'ORDER' or message_received['method'] == 'PICKUP':
      if message_received['method'] == 'ORDER':
         new_message['method'] = ORDER
         new_message['args']['food'] = choose_food_class(message_received['args'])
         new_message['args']['address'] = addr
      else:
         new_message['method'] = PICKUP
         new_message['args'] = message_received['args']
   else:
      new_message = message_received

   return new_message
