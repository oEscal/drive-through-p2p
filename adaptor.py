from food import Hamburger, Chips, Drink
from utils import ORDER, PICKUP, GIVE_FOOD
from encapsulation_utils import nodes_message_create, order_food_message_create


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

   # converts the dictionary sent by the professor's client to a list
   # with the correspondent Object food and number, that can be interpreted
   # by our RingNode
   def foodStringToFoodObject(self, all_food):
      food_class_list = []

      for food in all_food:
         if food in self.prof_food_names_to_object:
            food_class_list.append(self.prof_food_names_to_object[food](all_food[food]))

      return food_class_list

   # takes the list with the food objects, and converts it to a dictionary
   # with the same syntax as the professor's food list
   def foodObjectToFoodString(self, all_food):
      result = {k: 0 for k in self.prof_food_names_to_object}

      for food in all_food:
         if food.__class__ in self.object_food_names_to_prof:
            result[self.object_food_names_to_prof[food.__class__]] = food.number

      return result

   # convert the messages sent by the professor's client to the correspondent
   # messages that can be analysed by our RingNode
   def adapt(self, message_received, addr):
      message_order_food = order_food_message_create(None, None)
      new_message = nodes_message_create(None, message_order_food)

      if (message_received['method'] == 'ORDER' or message_received['method'] == 'PICKUP'
         or message_received['method'] == GIVE_FOOD):
         if message_received['method'] == 'ORDER':
            new_message['method'] = ORDER
            new_message['args']['food'] = self.foodStringToFoodObject(message_received['args'])
            new_message['args']['address'] = addr

         elif message_received['method'] == 'PICKUP':
            new_message['method'] = PICKUP
            new_message['args'] = message_received['args']
      else:
         new_message = message_received

      return new_message
