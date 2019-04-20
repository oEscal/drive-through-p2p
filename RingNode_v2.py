# coding: utf-8

import time
import socket
import threading
import logging
import pickle
import queue
from utils import NODE_JOIN, REQUEST_INFO, ENTITIES_NAMES, NODE_DISCOVERY, ORDER, PICKUP, TOKEN, PICK, KEEP_ALIVE, IM_ALIVE

class RingNode(threading.Thread):
   def __init__(self, address, id, name, max_nodes=4, ring_address=None, timeout=3, refresh_time=3):
      threading.Thread.__init__(self)
      self.id = id
      self.addr = address
      self.ring_address = ring_address
      self.max_nodes = max_nodes

      self.inside_ring = False
      self.successor_id = self.max_nodes*2
      self.successor_addr = self.addr
      self.nodes_com = []
      self.name = name

      self.refresh_time = refresh_time

      self.entities = {}
      for i in range(len(ENTITIES_NAMES)):
         self.entities[ENTITIES_NAMES[i]] = None

      self.coordinator = False

      self.inside_ring_order = 0

      # queues
      self.in_queue = queue.Queue()                      # messages received from the token
      self.out_queue = queue.Queue()                     # messages to send to the token

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

   def broadcast(self, message_to_send):
      for i in range(254):
         address_send = ('127.0.0.' + str(i + 1), 5000)
         self.send(address_send, message_to_send)

   def requestJoin(self):
      # send info about me to other nodes
      message_to_send = {'method': NODE_JOIN, 'args': {'addr': self.addr, 'id': self.id}}
      self.broadcast(message_to_send)

   def requestInfo(self):
      # request info about other nodes (because they can already be in
      # the ring and this is to accelerate the process of enter the ring)
      message_to_send = {'method': REQUEST_INFO, 'args': {'addr': self.addr, 'id': self.id}}
      self.broadcast(message_to_send)

   def discoveryReply(self, args):
      message_to_send = {'method': NODE_DISCOVERY, 'args': args.copy()}

      if self.name == args['name'] and args['id'] is None:
         message_to_send['args']['id'] = self.id
      elif args['id'] is not None:
         self.entities[args['name']] = args['id']
         # self.logger.debug('My table of entities: ' + str(self.entities))

      if args['id'] != self.id:
         self.send(self.successor_addr, message_to_send)

   def allNodesDiscovered(self):
      number_nodes = 0
      for i in self.entities:
         if self.entities[i] is not None:
            number_nodes += 1
      return number_nodes == self.max_nodes

   def sendMessageToToken(self, id, order):
      message_to_send = {
         'method': TOKEN,
         'args': {
            'id': id,
            'order': order
         }
      }
      self.out_queue.put(message_to_send)

   def run(self):
      self.socket.bind(self.addr)

      delta_time = time.time()
      im_alive_time = time.time()
      time_since_last_alive = time.time()
      token_sent = False

      while True:
         p, addr = self.recv()
         if p is not None:
            message_received = pickle.loads(p)

            if message_received['method'] == REQUEST_INFO:
               message_to_send = {'method': NODE_JOIN, 'args': {'addr': self.addr, 'id': self.id}}
               self.send(message_received['args']['addr'], message_to_send)
            if message_received['method'] == NODE_JOIN or message_received['method'] == REQUEST_INFO:
               args = message_received['args']

               if args['id'] not in self.nodes_com:
                  self.nodes_com.append(args['id'])

               if args['id'] < self.id:
                  self.coordinator = False
               if self.id <= min(self.nodes_com):
                  self.coordinator = True

               if args['id'] > self.successor_id and self.successor_id < self.id and len(self.nodes_com) > self.id + 1:
                  self.inside_ring = False
                  self.successor_id = self.max_nodes*2
                  self.successor_addr = self.addr

               if (len(self.nodes_com) > 1 and self.id == max(self.nodes_com) and args['id'] == min(self.nodes_com)
                       or self.successor_id > args['id'] > self.id):
                  self.inside_ring = True
                  self.successor_id = args['id']
                  self.successor_addr = args['addr']
                  time_since_last_alive = time.time()

                  self.logger.debug("Me: " + str(self.addr) + "\nSuccessor:" + str(self.successor_addr) + "\n")

            elif message_received['method'] == KEEP_ALIVE:
               message_to_send = {
                  'method': IM_ALIVE,
                  'args': None
               }
               self.send(addr, message_to_send)
            elif message_received['method'] == IM_ALIVE:
               time_since_last_alive = time.time()
            elif message_received['method'] == NODE_DISCOVERY:
               self.discoveryReply(message_received['args'])
            elif message_received['method'] == ORDER:
               self.logger.debug("Message received from client: " + str(message_received))
               self.sendMessageToToken(self.entities['Waiter'], message_received['args'])
            elif message_received['method'] == PICKUP:
               self.logger.debug("Message received from client: " + str(message_received))

               message_to_send = {
                  'type': PICK,
                  'value': message_received['args']
               }
               self.sendMessageToToken(self.entities['Clerk'], message_to_send)
            elif message_received['method'] == TOKEN:
               id_destination = message_received['args']['id']
               message_to_send = message_received

               if id_destination == self.id:
                  self.in_queue.put(message_received['args']['order'])
                  message_to_send = {
                     'method': TOKEN,
                     'args': {
                        'id': None,
                        'order': None
                     }
                  }

               if self.out_queue.qsize() > 0 and (id_destination == self.id
                  or id_destination is None):
                  message_to_send = self.out_queue.get()

               if len(self.nodes_com) == self.max_nodes:
                  self.send(self.successor_addr, message_to_send)
               else:
                  self.logger.debug("TOKEN REMOVED!")
            else:
               self.send(self.successor_addr, message_received)

         if not self.inside_ring:
            self.requestInfo()

         if self.inside_ring and time.time() - im_alive_time > self.refresh_time:
            im_alive_time = time.time()

            message_to_send = {
               'method': KEEP_ALIVE,
               'args': None
            }

            self.send(self.successor_addr, message_to_send)

         if self.inside_ring and time.time() - time_since_last_alive > self.refresh_time*2:
            if self.successor_id in self.nodes_com:
               self.nodes_com.pop(self.nodes_com.index(self.successor_id))

            self.inside_ring = False
            self.successor_id = self.max_nodes * 2
            self.successor_addr = self.addr
            token_sent = False

         if self.coordinator and self.inside_ring and len(self.nodes_com) == self.max_nodes:
            if not self.allNodesDiscovered():
               for i in self.entities:
                  if self.entities[i] is None:
                     message_to_send = {'method': NODE_DISCOVERY, 'args': {'name': i, 'id': None}}
                     self.send(self.successor_addr, message_to_send)
            elif not token_sent:
               message_to_send = {
                  'method': TOKEN,
                  'args': {
                     'id': None,
                     'order': None
                  }
               }
               self.send(self.successor_addr, message_to_send)
               token_sent = True
               self.logger.debug("TOKEN SENT BEFORE %s SECONDS!", str(time.time() - delta_time))