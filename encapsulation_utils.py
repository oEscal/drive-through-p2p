from message_encapsulation import *

def nodes_message_create(method, args):
   message_copy = nodes_message.copy()
   message_copy['method'] = method
   message_copy['args'] = args
   return message_copy

def token_message_create(ide, order):
   message_copy = token_message.copy()
   message_copy['id'] = ide
   message_copy['order'] = order
   return message_copy

def pre_ring_message_create(addr, ide):
   message_copy = pre_ring_message.copy()
   message_copy['addr'] = addr
   message_copy['id'] = ide
   return message_copy

def discovery_message_create(name, ide):
   message_copy = discovery_message.copy()
   message_copy['name'] = name
   message_copy['id'] = ide
   return message_copy

def order_food_message_create(addr, food):
   message_copy = order_food_message.copy()
   message_copy['addr'] = addr
   message_copy['food'] = food
   return message_copy

def entities_message_create(type_, value):
   message_copy = entities_message.copy()
   message_copy['type'] = type_
   message_copy['value'] = value
   return message_copy

def waiter_to_chef_message_create(client_address, ticket, food):
   message_copy = waiter_to_chef_message.copy()
   message_copy['client_address'] = client_address
   message_copy['ticket'] = ticket
   message_copy['food'] = food
   return message_copy
