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
from kitchen_equipments import Grill, Fryer, Fridge
from utils import REQUEST_GRILL, REQUEST_FRIDGE, REQUEST_FRYER, ACKNOWLEDGE


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M:%S')
logger = logging.getLogger('Restaurant')


class Restaurant(threading.Thread):
   def __init__(self, number_grills=1, number_fryers=1, number_fridges=1, port=5000, ide=0):
      threading.Thread.__init__(self)
      self.id = ide
      self.port = port

      self.name = self.__class__.__name__
      self.node = RingNode(('127.0.0.' + str(1 + self.id), 5000), self.id, self.name)

      # equipments
      self.grills = queue.Queue()
      self.fryers = queue.Queue()
      self.fridges = queue.Queue()

      for i in range(number_grills):
         self.grills.put(Grill())
      for i in range(number_fryers):
         self.fryers.put(Fryer())
      for i in range(number_fridges):
         self.fridges.put(Fridge())

   def run(self):
      self.node.start()

      while True:
         request = self.node.in_queue.get()  # request do chef para uso de equipamentos
         logger.debug("Received new message: " + str(request))
         if 'type' not in request:
            current_index = 0
            while True:
               request_eq = request[current_index]

               if request_eq == REQUEST_GRILL:
                  if self.grills.qsize() > 0:
                     eq = self.grills.get()
                     break
               elif request_eq == REQUEST_FRYER:
                  if self.fryers.qsize() > 0:
                     eq = self.fryers.get()
                     break
               elif request_eq == REQUEST_FRIDGE:
                  if self.fridges.qsize() > 0:
                     eq = self.fridges.get()
                     break

               current_index += 1
               current_index %= len(request)

            message_to_send = {
               'type': ACKNOWLEDGE,
               'value': eq
            }

            self.node.sendMessageToToken(self.node.entities['Chef'], message_to_send)
            logger.debug("Equipment sent: " + str(eq))

         else:
            if request['value'].__class__ == Grill:
               self.grills.put(request['value'])
            elif request['value'].__class__ == Fryer:
               self.fryers.put(request['value'])
            elif request['value'].__class__ == Fridge:
               self.fridges.put(request['value'])

            logger.debug("Received the equipment " + str(request['value']))
