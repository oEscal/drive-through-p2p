# coding: utf-8

import random
import uuid
import time
import logging
import threading
from RingNode import RingNode
from utils import NEW_ORDER, TICKET, print_out

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M:%S')
logger = logging.getLogger('Waiter')


class Waiter(threading.Thread):
   def __init__(self, ide=1):
      threading.Thread.__init__(self)
      self.id = ide

      self.mean = 2
      self.std = 0.5

      self.name = self.__class__.__name__
      self.node = RingNode(('127.0.0.' + str(1 + self.id), 5000), self.id, self.name)

   def run(self):
      self.node.start()

      while True:
         # receive a new client's order
         orders = self.node.in_queue.get()
         logger.debug("Received new order from client: " + print_out(orders['food']))

         # verify if there are empty orders
         order_to_cooker = []
         for food in orders['food']:
            if food.number != 0:
               order_to_cooker.append(food)

         # work time
         time.sleep(random.gauss(self.mean, self.std))

         if len(order_to_cooker) != 0:
            ticket = uuid.uuid1()

            # send request to chef
            message_to_send = {
               'type': NEW_ORDER,
               'value': {
                  'client_address': orders['address'],
                  'ticket': ticket,
                  'food': order_to_cooker
               }
            }

            self.node.sendMessageToToken(self.node.entities['Chef'], message_to_send)
            logger.debug("Chef order sent: " + print_out(order_to_cooker))


            # send the ticket to the client
            message_to_send = {
               'type': TICKET,
               'args': ticket
            }
            self.node.send(orders['address'], message_to_send)

