# coding: utf-8

import logging
import threading
import queue
import copy
from RingNode import RingNode
from food import Hamburger, Chips, Drink
from utils import REQUEST_GRILL, REQUEST_FRIDGE, REQUEST_FRYER, ACKNOWLEDGE, RETURN_EQ, NEW_ORDER, FOOD_DONE, print_out, print_equipment_requests

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M:%S')
logger = logging.getLogger('Chef')


class Chef(threading.Thread):
   def __init__(self, port=5002, ide=2):
      threading.Thread.__init__(self)
      self.id = ide
      self.port = port

      self.name = self.__class__.__name__
      self.node = RingNode(('127.0.0.' + str(1 + self.id), 5000), self.id, self.name)

      self.pending_orders = queue.Queue()

      self.last_order = None
      self.order_to_client = {}

   def choose_request(self, food): #return request value according to the food
      if food.__class__ == Hamburger:
         return REQUEST_GRILL
      elif food.__class__ == Drink:
         return REQUEST_FRIDGE
      elif food.__class__ == Chips:
         return REQUEST_FRYER
      return None


   def requests(self, order): #chef do request to the restaurant to equipment usage
      equipments_to_request = []
      
      for food in order:
         equipments_to_request.append(self.choose_request(food))
      # send all equipments needed to cook the client's order
      if len(equipments_to_request) > 0:
         self.node.sendMessageToToken(self.node.entities['Restaurant'], equipments_to_request)
         logger.debug("Requesting %s", print_equipment_requests(equipments_to_request))

   def cook(self, equipment, food): #cooking function,after the necessary ack
      equipment.cook(food.number)
      logger.debug("I cooked %s!\n", str(food))

      self.order_to_client['food'].append(food)

   def run(self):
      self.node.start()

      while True:
         #recieving ACK orders from restaurant or food requests from waiter to be cooked
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
                  #recieve the ACK from restaurant and then cooks the food
                  self.cook(orders['value'], self.last_order[i])
                  self.last_order.pop(i)

                  # return the equipment to the restaurant
                  message_to_send = {
                     'type': RETURN_EQ,
                     'value': orders['value']
                  }
                  self.node.sendMessageToToken(self.node.entities['Restaurant'], message_to_send)

                  self.requests(self.last_order)
                  break

         if self.last_order is not None and len(self.last_order) == 0:
            # inform the clerk that the food is done
            message_to_send = {
               'type': FOOD_DONE,
               'value': self.order_to_client
            }
            
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
