import logging
from RingNode import RingNode
from utils import ENTITIES_NAMES

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M:%S')


class Receptionist:
   def __init__(self):
      self.id = 1
      self.name = ENTITIES_NAMES[self.id]
      self.node = RingNode(('127.0.0.' + str(1 + self.id), 5000), self.id, self.name)

   def start_node(self):
      self.node.start()


def main():
   logger = logging.getLogger('restaurant')

   restaurant = Receptionist()
   restaurant.start_node()
   logger.debug('started')

main()