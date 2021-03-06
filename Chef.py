# coding: utf-8

import logging
import threading
import queue
import copy
from RingNode import RingNode
from food import Hamburger, Chips, Drink
from utils import REQUEST_GRILL, REQUEST_FRIDGE, REQUEST_FRYER, ACKNOWLEDGE, RETURN_EQ, \
   NEW_ORDER, FOOD_DONE, print_out
from message_encapsulation import entities_message

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M:%S')
logger = logging.getLogger('Chef')


class Chef(threading.Thread):
   def __init__(self, ide=2):
      threading.Thread.__init__(self)
      self.id = ide

      self.name = self.__class__.__name__
      self.node = RingNode(('127.0.0.' + str(1 + self.id), 5000), self.id, self.name)

      self.pending_orders = queue.Queue()

      self.last_order = None
      self.order_to_client = {}

   # returns request value according to the food
   def choose_request(self, food):
      if food.__class__ == Hamburger:
         return REQUEST_GRILL
      elif food.__class__ == Drink:
         return REQUEST_FRIDGE
      elif food.__class__ == Chips:
         return REQUEST_FRYER
      return None

   # chef do request to the restaurant to equipment usage
   def requests(self, order):
      equipments_to_request = []
      for food in order:
         equipments_to_request.append(self.choose_request(food))

      # send all equipments needed to cook the client's order
      if len(equipments_to_request) > 0:
         self.node.sendMessageToToken(self.node.entities['Restaurant'], equipments_to_request)
         logger.debug("Requesting %s", equipments_to_request)

   # cooking function,after the necessary ack
   def cook(self, equipment, food):
      equipment.cook(food.number)
      logger.debug("I cooked %s!\n", str(food))

      self.order_to_client['food'].append(food)

   def run(self):
      self.node.start()

      while True:
         # receiving ACK orders from restaurant or food requests from waiter to be cooked
         orders = self.node.in_queue.get()

         if orders['type'] == NEW_ORDER:
            message_received_copy = copy.deepcopy(orders['value'])
            message_received_copy['food'] = print_out(message_received_copy['food'])

            logger.debug("Received new order from waiter: " + str(message_received_copy))
            self.pending_orders.put(orders['value'])  # save requests in queue

         elif orders['type'] == ACKNOWLEDGE and self.last_order is not None:
            logger.debug("Received equipment: " + str(orders['value']))
            equipment_received_class = orders['value'].__class__

            for i in range(len(self.last_order)):
               current_food_equipment_class = self.last_order[i].equipment_required_to_cook.__class__

               if current_food_equipment_class == equipment_received_class:
                  # receive the ACK from restaurant and then cooks the food
                  self.cook(orders['value'], self.last_order[i])
                  self.last_order.pop(i)

                  # return the equipment to the restaurant
                  message_to_send = entities_message.copy()
                  message_to_send['type'] = RETURN_EQ
                  message_to_send['value'] = orders['value']

                  self.node.sendMessageToToken(self.node.entities['Restaurant'], message_to_send)

                  self.requests(self.last_order)
                  break

         if self.last_order is not None and len(self.last_order) == 0:
            # inform the clerk that the food is done
            message_to_send = entities_message.copy()
            message_to_send['type'] = FOOD_DONE
            message_to_send['value'] = self.order_to_client

            message_received_copy = copy.deepcopy(message_to_send)
            message_received_copy['value']['food'] = print_out(message_received_copy['value']['food'])

            self.node.sendMessageToToken(self.node.entities['Clerk'], message_to_send)    #send the request to clerk
            logger.debug("Sending to clerk : %s", str(message_received_copy))
            self.last_order = None
            self.order_to_client = {}

         if self.last_order is None and not self.pending_orders.empty():
            new_order = self.pending_orders.get()

            self.order_to_client['ticket'] = new_order['ticket']
            self.order_to_client['client_address'] = new_order['client_address']
            self.order_to_client['food'] = []
            self.last_order = new_order['food']

            self.requests(self.last_order)