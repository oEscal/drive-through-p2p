import time
import logging
from RingNode import RingNode
from utils import ENTITIES_NAMES, RING_FORMED, NODE_DISCOVERY

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M:%S')


class Restaurant(RingNode):
   id = 0
   name = ENTITIES_NAMES[id]
   def __init__(self):
      super().__init__(('127.0.0.' + str(1 + self.id), 5000), self.id, self.name)

   def allInRing(self):
      return self.max_nodes == len(self.nodes_com)




def main():
   logger = logging.getLogger('restaurant')

   # start
   restaurant = Restaurant()
   restaurant.start()
   logger.debug('started')

   # I need this block of code because we can just switch three (or less) of the four entities
   delta_time = time.time()
   while restaurant.inside_ring_order != restaurant.max_nodes:
      if restaurant.inside_ring and time.time() - delta_time > 2:
         message_to_send = {'method': RING_FORMED, 'args': 0}
         restaurant.send(restaurant.successor_addr, message_to_send)
         delta_time = time.time()

   discovery = True
   while discovery:
      if restaurant.allInRing():
         for i in restaurant.entities:
            message_to_send = {'method': NODE_DISCOVERY, 'args': {'name': i, 'id': None}}
            restaurant.send(restaurant.successor_addr, message_to_send)
         discovery = False

main()