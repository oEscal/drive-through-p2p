# coding: utf-8

import logging
import threading
import copy
import time
from RingNode import RingNode
from utils import FOOD_DONE, PICKUP, GIVE_FOOD, print_out

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M:%S')
logger = logging.getLogger('Clerk')


class Clerk(threading.Thread):
   def __init__(self, ide=3):
      threading.Thread.__init__(self)
      self.id = ide

      self.name = self.__class__.__name__
      self.node = RingNode(('127.0.0.' + str(1 + self.id), 5000), self.id, self.name)

      self.food_cold_timeout = 10
      self.food_done = {}
      self.pickups = []

   def class_into_dict(self, food):
      food_dict = {}
      for i in food:
         food_dict[i.name] = i.number
      return food_dict

   def set_order(self):  # forward the food order to its customer
      for client_id in self.pickups:
         if client_id in self.food_done:
            logger.debug("Given food %s to %s", print_out(self.food_done[client_id][1]), str(client_id))

            self.node.sendToClient(self.food_done[client_id][0], self.food_done[client_id][1])

            print(self.food_done[client_id][1])
            print(self.class_into_dict(self.food_done[client_id][1]))
            self.food_done.pop(client_id)  # to remove the given food
            self.pickups.remove(client_id)  # remove client_id picked

   def check_food_state(
         self):  # tests whether the food remains hot using a timeout variable(defined above ->self.food_cold_timeout)
      food_done_copy = copy.deepcopy(self.food_done)
      for key in food_done_copy:
         if time.time() - self.food_done[key][-1] > self.food_cold_timeout:
            self.food_done.pop(key)

   def run(self):
      self.node.start()

      while True:
         request = self.node.in_queue.get()

         if request['type'] == FOOD_DONE:  # add ready food orders in a queue
            message_received_copy = copy.deepcopy(request)
            message_received_copy['value']['food'] = print_out(message_received_copy['value']['food'])

            logger.debug("Food done %s", str(message_received_copy))

            self.food_done[request['value']['ticket']] = (
               request['value']['client_address'], request['value']['food'], time.time()
            )


         elif request['type'] == PICKUP:  # add customers ready for payment in a list
            logger.debug("Pickup request %s", request['value'])
            self.pickups.append(request['value'])

         if len(self.pickups) > 0 and len(self.food_done) > 0:
            self.set_order()

         if len(self.food_done) > 0:
            self.check_food_state()
