from food import Hamburger, Chips, Drink
from utils import ORDER, PICKUP, GIVE_FOOD


class Adaptor:
   def __init__(self):
      self.prof_food_names_to_object = {
         'hamburger': Hamburger,
         'fries': Chips,
         'drink': Drink
      }
      self.object_food_names_to_prof = {
         v: k for k, v in self.prof_food_names_to_object.items()
      }

      self.prof_clients_received = []

   def foodStringToFoodObject(self, all_food):
      food_class_list = []

      for food in all_food:
         if food in self.prof_food_names_to_object:
            food_class_list.append(self.prof_food_names_to_object[food](all_food[food]))

      return food_class_list

   def foodObjectToFoodString(self, all_food):
      result = {k: 0 for k in self.prof_food_names_to_object}

      for food in all_food:
         if food.__class__ in self.object_food_names_to_prof:
            result[self.object_food_names_to_prof[food.__class__]] = food.number

      return result

   def adapt(self, message_received, addr):
      new_message = {
         'method': None,
         'args': {
            'food': None,
            'address': None
         }
      }
      if (message_received['method'] == 'ORDER' or message_received['method'] == 'PICKUP'
         or message_received['method'] == GIVE_FOOD):
         if message_received['method'] == 'ORDER':
            new_message['method'] = ORDER
            new_message['args']['food'] = self.foodStringToFoodObject(message_received['args'])
            new_message['args']['address'] = addr

            self.prof_clients_received.append(addr)
         elif message_received['method'] == 'PICKUP':
            new_message['method'] = PICKUP
            new_message['args'] = message_received['args']
         else:
            if addr in self.prof_clients_received:
               new_message['method'] = 'GIVE_FOOD'
               new_message['args'] = self.foodObjectToFoodString(message_received['args'])
            else:
               new_message = message_received
      else:
         new_message = message_received

      return new_message
