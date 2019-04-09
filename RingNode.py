# coding: utf-8

import time
import socket
import threading
import logging
import pickle
from utils import dht_hash, contains_predecessor, contains_successor


class RingNode(threading.Thread):
   def __init__(self, address, id, max_nodes=4, dht_address=None, timeout=3):
      threading.Thread.__init__(self)
      self.id = id
      self.addr = address
      self.dht_address = dht_address
      self.max_nodes = max_nodes

      self.inside_dht = False
      self.successor_id = self.max_nodes*2
      self.successor_addr = self.addr
      self.nodes_com = []

      self.keystore = {}
      self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
      self.socket.settimeout(timeout)
      self.logger = logging.getLogger("Node {}".format(self.id))

   def send(self, address, o):
      p = pickle.dumps(o)
      self.socket.sendto(p, address)

   def recv(self):
      try:
         p, addr = self.socket.recvfrom(1024)
      except socket.timeout:
         return None, None
      else:
         if len(p) == 0:
            return None, addr
         else:
            return p, addr

   def put(self, key, value, address):
      key_hash = dht_hash(key)
      self.logger.debug('Put: %s %s', key, key_hash)
      if contains_successor(self.id, self.successor_id, key_hash):
         self.keystore[key] = value
         self.send(address, {'method': 'ACK'})
      else:
         # send to DHT
         self.send(self.successor_addr, {'method': 'PUT', 'args': {'key': key, 'value': value, 'addr': address}})

   def get(self, key, address):
      key_hash = dht_hash(key)
      self.logger.debug('Get: %s %s', key, key_hash)
      if contains_successor(self.id, self.successor_id, key_hash):
         value = self.keystore[key]
         self.send(address, {'method': 'ACK', 'args': value})
      else:
         # send to DHT
         self.send(self.successor_addr, {'method': 'GET', 'args': {'key': key, 'addr': address}})

   def requestJoin(self):
      o = {'method': 'NODE_JOIN', 'args': {'addr': self.addr, 'id': self.id}}
      for i in range(254):
         address_send = ('127.0.0.' + str(i + 1), 5000)
         #print(address_send)
         self.send(address_send, o)

   def run(self):
      self.socket.bind(self.addr)

      delta_time = time.time()
      while True:
         p, addr = self.recv()
         if p is not None:
            message_received = pickle.loads(p)
            #self.logger.info('O: %s', message_received)
            if message_received['method'] == 'NODE_JOIN':
               args = message_received['args']

               if args['id'] not in self.nodes_com:
                  self.nodes_com.append(args['id'])

               if args['id'] > self.successor_id < self.id and len(self.nodes_com) > self.id + 1:
                  self.inside_dht = False
                  self.successor_id = self.max_nodes*2
                  self.successor_addr = self.addr

               if self.successor_id > args['id'] > self.id:
                  self.inside_dht = True
                  self.successor_id = args['id']
                  self.successor_addr = args['addr']

               elif (len(self.nodes_com) > 1 and
                       self.id == max(self.nodes_com) and args['id'] == min(self.nodes_com)):
                  self.inside_dht = True
                  self.successor_id = args['id']
                  self.successor_addr = args['addr']

            if message_received['method'] == 'JOIN_REQ':
               self.node_join(message_received['args'])

         if not self.inside_dht or time.time() - delta_time > 2:
            self.requestJoin()
            delta_time = time.time()

            print(str(self.addr))
            print(str(self.successor_addr) + "\n")
