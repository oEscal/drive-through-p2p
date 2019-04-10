import logging
from RingNode import RingNode
from utils import ENTITIES_NAMES

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M:%S')


class Receptionist(RingNode):
   id = 1
   name = ENTITIES_NAMES[id]
   def __init__(self):
      super().__init__(('127.0.0.' + str(1 + self.id), 5000), self.id, self.name)


def main():
   logger = logging.getLogger('restaurant')

   restaurant = Receptionist()
   restaurant.start()
   logger.debug('started')

main()