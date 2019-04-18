# coding: utf-8

import time
import pickle
import socket
import random
import logging
import argparse
import threading
import queue
from RingNode import RingNode
from food import Food
from kitchen_equipments import KitchenEquipment
from utils import REQUEST_GRILLER, REQUEST_FRIDGE, REQUEST_FRYER

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M:%S')
logger = logging.getLogger('Chef')


class Chef(threading.Thread):
    def __init__(self, port=5002, ide=2):
        threading.Thread.__init__(self)
        self.id = ide
        self.port = port

        self.name = self.__class__.__name__
        self.node = RingNode(('127.0.0.' + str(1 + self.id), 5000), self.id, self.name)

        self.pending_orders = queue.Queue() 

        self.last_order = None

    def choose_request(self,food): #escolhe o request a ser feito dependendo do tipo de comida
        if food.name == "hamburger":
            return REQUEST_GRILLER
        elif food.name == "drink":
            return REQUEST_FRIDGE
        return REQUEST_FRYER

    def ready(self,order): #return TRue, se o pedido tiver pronto (ou seja tudo cozinhado)
        for food in order:
            if not food.cooked:   
                return False
        return True

    def requests(self,order): #o chef faz request ao server para uso de equipamentos
        for food in order:
            if not food.cooked:
                request = self.choose_request(food)
                self.node.sendMessageToToken(self.node.entities['Restaurant'],{'value':request})
                logger.debug("Requesting %s",request)
    

    def cook(self,ack_value,order): # o chef no fim de receber ACK do restaurante do uso de equipamentos , cozinha
        for food in order:
            if food.equipment_required_to_cook.request_number == ack_value - 100:
                food.equipment_required_to_cook.cook(food.number)
                logger.debug("Cooking %s",food)
                food.cooked = True 
                

    def run(self):
            self.node.start()

            while True:

                orders = self.node.in_queue.get() #receber ordens de ACK do restaurante ou de REQ do waiter


                if orders['type'] == 'ACK' and self.last_order is not None:
                    logger.debug("ACK -> %d",orders['value'])
                    self.cook(orders['value'],self.last_order['food']) #recebe o ACK do uso de equipamente do restaurante e cozinha a comida respetiva
                
                elif orders['type'] == 'REQ':
                    logger.debug("Received new order from waiter: " + str(orders['value']))
                    self.pending_orders.put(orders['value']) #guarda os pedidos numa fila
                
                if self.last_order is not None:
                    if self.ready(self.last_order['food']): #significa que o pedido esta pronto
                        self.node.sendMessageToToken(self.node.entities['Clerk'], {'type':'FOOD_DONE','value':self.last_order} ) # envia o pedido para o clerk
                        logger.debug("Sending to clerk : %s",self.last_order)
                        self.last_order = None
                    if not self.pending_orders.empty():
                        self.last_order = self.pending_orders.get() 
                else:
                    if not self.pending_orders.empty():
                        self.last_order = self.pending_orders.get() 
                    
                    
                if self.last_order is not None:
                    self.requests(self.last_order['food'])

