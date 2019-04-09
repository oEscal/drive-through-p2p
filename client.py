import logging
from DHT_Node import DHT_Node

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M:%S')


class Client(DHT_Node):
   id = 4
   def __init__(self):
      super().__init__(('127.0.0.' + str(1 + self.id), 5000), ('<broadcast>', 5000))


def main():
   logger = logging.getLogger('client')

   restaurant = Client()
   restaurant.start()
   logger.debug('started')

main()