# coding: utf-8

import time
import pickle
import socket
import random
import logging
import argparse
import threading
import queue
from RingNode import RingNode
from utils import FOOD_DONE, PICK

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M:%S')
logger = logging.getLogger('Clerk')


class Clerk(threading.Thread):
   def __init__(self, port=5003, ide=3):
      threading.Thread.__init__(self)
      self.id = ide
      self.port = port

      self.name = self.__class__.__name__
      self.node = RingNode(('127.0.0.' + str(1 + self.id), 5000), self.id, self.name)

      self.food_done = queue.Queue()
      self.pickups = []
      
   def set_order(self, food):    # reencaminhar a ordem de comida para o respetivo cliente
      for client_id in self.pickups:
         if client_id == food['ticket']:
            logger.debug("Given food %s to %s", str(food['food']), str(client_id))
            self.node.send(food['client_address'], {'type': 'GIVEN', 'args': food['food']})
            self.food_done.get()    # to remove the given food
            self.pickups.remove(client_id)   # remove client_id picked
   
   def run(self):
      self.node.start()

      while True:
         request = self.node.in_queue.get()

         if request['type']  == FOOD_DONE:   # adicionar numa fila os pedidos de comida prontos
             logger.debug("Food done %s", request['value'])
             self.food_done.put(request['value'])
         elif request['type'] == PICK: # adicionar numa lista os clientes prontos para pagamento
             logger.debug("Pickup request %s",request['value'])
             self.pickups.append(request['value'])

         if len(self.pickups) > 0 and not self.food_done.empty():
             self.set_order(self.food_done.queue[0])
