# coding: utf-8

import time
import pickle
import socket
import random
import logging
import argparse
import threading
from RingNode import RingNode
from food import Food
from kitchen_equipments import KitchenEquipment

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

   def run(self):
      self.node.start()

      while True:
         # receive a new waiter's order
         orders = self.node.in_queue.get()
         logger.debug("Received new order from waiter: " + str(orders))

