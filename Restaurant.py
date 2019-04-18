# coding: utf-8

import time
import pickle
import socket
import random
import logging
import argparse
import threading
from RingNode import RingNode
from utils import REQUEST_GRILLER, REQUEST_FRIDGE, REQUEST_FRYER


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M:%S')
logger = logging.getLogger('Restaurant')


class Restaurant(threading.Thread):
   def __init__(self, port=5000, ide=0):
      threading.Thread.__init__(self)
      self.id = ide
      self.port = port

      self.name = self.__class__.__name__
      self.node = RingNode(('127.0.0.' + str(1 + self.id), 5000), self.id, self.name)

   def run(self):
        self.node.start()

        while True:
            request = self.node.in_queue.get() #request do chef para uso de equipamentos
            self.node.sendMessageToToken(self.node.entities['Chef'],{'type':'ACK','value':request['value'] + 100}) #request + 100 -> ACK value from restaurant
            logger.debug("Sending ACK for %d -> %d",request['value'],request['value'] + 100)


