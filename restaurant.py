import logging
from RingNode import RingNode

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M:%S')


class Restaurant(RingNode):
   id = 0
   def __init__(self):
      super().__init__(('127.0.0.' + str(1 + self.id), 5000), self.id)


def main():
   logger = logging.getLogger('restaurant')

   restaurant = Restaurant()
   restaurant.start()
   logger.debug('started')

main()