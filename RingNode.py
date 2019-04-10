# coding: utf-8

import time
import socket
import threading
import logging
import pickle
from utils import NODE_JOIN, ENTITIES_NAMES, JOIN_REQ, RING_FORMED, NODE_DISCOVERY

class RingNode(threading.Thread):
   def __init__(self, address, id, name, max_nodes=4, ring_address=None, timeout=3):
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

      self.entities = {}
      for i in range(len(ENTITIES_NAMES)):
         self.entities[ENTITIES_NAMES[i]] = None

      self.inside_ring_order = 0

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

   def requestJoin(self):
      message_to_send = {'method': NODE_JOIN, 'args': {'addr': self.addr, 'id': self.id}}

      # multicast
      for i in range(254):
         address_send = ('127.0.0.' + str(i + 1), 5000)
         self.send(address_send, message_to_send)

   def discoveryReply(self, args):
      message_to_send = {'method': NODE_DISCOVERY, 'args': args.copy()}

      if self.name == args['name'] and args['id'] is None:
         message_to_send['args']['id'] = self.id
      elif args['id'] is not None:
         self.entities[args['name']] = args['id']
         print(args['name'])
         print(args['id'])
         self.logger.debug('My table of entities: ' + str(self.entities))

      if args['id'] != self.id:
         self.send(self.successor_addr, message_to_send)

   def run(self):
      self.socket.bind(self.addr)

      delta_time = time.time()
      while True:
         p, addr = self.recv()
         if p is not None:
            message_received = pickle.loads(p)
            if message_received['method'] == NODE_JOIN:
               args = message_received['args']

               if args['id'] not in self.nodes_com:
                  self.nodes_com.append(args['id'])

               # depois olhar para este if que pode ser melhorado
               if args['id'] > self.successor_id < self.id and len(self.nodes_com) > self.id + 1:
                  self.inside_ring = False
                  self.successor_id = self.max_nodes*2
                  self.successor_addr = self.addr

               if ((len(self.nodes_com) > 1 and
                       self.id == max(self.nodes_com) and args['id'] == min(self.nodes_com)) or
                       self.successor_id > args['id'] > self.id):
                  self.inside_ring = True
                  self.successor_id = args['id']
                  self.successor_addr = args['addr']
            elif message_received['method'] == JOIN_REQ:
               self.node_join(message_received['args'])
            elif message_received['method'] == RING_FORMED:
               if self.inside_ring:
                  message_to_send = message_received
                  message_to_send['args'] += 1

                  self.inside_ring_order = message_to_send['args']

                  if self.inside_ring_order != len(self.nodes_com):
                     self.send(self.successor_addr, message_to_send)
            elif message_received['method'] == NODE_DISCOVERY:
               self.discoveryReply(message_received['args'])

         # depois meter um refresh time dado pelo user e não fixo no if
         if not self.inside_ring or time.time() - delta_time > 2:
            self.requestJoin()
            delta_time = time.time()

            self.logger.debug("Me: " + str(self.addr) + "\nSuccessor:" + str(self.successor_addr) + "\n")
