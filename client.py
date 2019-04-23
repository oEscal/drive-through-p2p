# coding: utf-8

import time
import pickle
import socket
import random
import logging
import argparse
from utils import ORDER, PICKUP, print_out, CAN_REQUEST, NOT_READY, READY
from food import Hamburger, Drink, Chips


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M:%S')

   

def main(port, ring, timeout):
   # Create a logger for the client
   logger = logging.getLogger('Client on port: ' + str(port))

   # UDP Socket
   sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   #sock.settimeout(timeout)
   sock.bind(('localhost', port))

   # Wait for a random time
   delta = random.gauss(2, 0.5)
   logger.info('Wait for %f seconds', delta)
   time.sleep(delta)


   #check if its possible to do requests
   while True:
      p = pickle.dumps({
               'method': CAN_REQUEST,
            })
      sock.sendto(p, ring)

      p, addr = sock.recvfrom(1024)
      o = pickle.loads(p)

      if o['type'] == READY:
         logger.debug("Ring Ready!!")
         break
      logger.debug("Ring not ready!!")
      logger.debug("Wait for %f seconds", delta)
      time.sleep(delta)

   # Request some food
   logger.info('Request some food...')
   p = pickle.dumps({
      'method': ORDER,
      'args': {'address': ('localhost', port), 'food': [
         Hamburger(random.randint(0, 5)),
         Drink(random.randint(0, 5)),
         Chips(random.randint(0, 5))
      ]}
   })

   logger.debug("Requesting %s", print_out(pickle.loads(p)['args']['food']))
   sock.sendto(p, ring)

   # Wait for Ticket
   p, addr = sock.recvfrom(1024)
   o = pickle.loads(p)
   logger.info('Received ticket %s', o['args'])

   # Pickup order
   logger.info('Pickup order %s', o['args'])
   p = pickle.dumps({"method": PICKUP, "args": o['args']})
   sock.sendto(p, ring)

   # Wait for order
   p, addr = sock.recvfrom(1024)
   o = pickle.loads(p)
   logger.info('Got order %s',print_out(o['args']))

   # Close socket
   sock.close()

   return 0


if __name__ == '__main__':
   parser = argparse.ArgumentParser(description='Pi HTTP server')
   parser.add_argument('-p', dest='port', type=int, help='client port', default=5004)
   parser.add_argument('-r', dest='ring', type=int, help='ring ports ', default=5000)
   parser.add_argument('-t', dest='timeout', type=int, help='socket timeout', default=30)
   args = parser.parse_args()
   main(args.port, ('localhost', args.ring), args.timeout)
