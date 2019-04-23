# messages's methods
NODE_JOIN = 0
REQUEST_INFO = 1
NODE_DISCOVERY = 2
ORDER = 3
PICKUP = 4
TOKEN = 5
TICKET = 6
KEEP_ALIVE = 7
IM_ALIVE = 8
CAN_REQUEST = 9
READY = 10
NOT_READY = 11

# request equipment
REQUEST_GRILL = 12
REQUEST_FRIDGE = 13
REQUEST_FRYER = 14

# message type to contact with the entities
NEW_ORDER = 0
ACKNOWLEDGE = 1
RETURN_EQ = 2
FOOD_DONE = 3
PICK = 4


# get by id
ENTITIES_NAMES = [
   'Restaurant',
   'Chef',
   'Clerk',
   'Waiter'
]

# equipment variables
GRILL_MEAN = 3
GRILL_STD = 0.5
FRIDGE_MEAN = 1
FRIDGE_STD = 0.5
FRYER_MEAN = 5
FRYER_STD = 0.5

#this 2 functions below, were made due to print facility, to cleary see what´s its happening
def print_out(request_input):
   string_order = ""
   for i in range(len(request_input)-1):
      string_order += str(request_input[i]) + ","
   string_order += str(request_input[len(request_input)-1])
   return string_order

def print_equipment_requests(array):
   equipments_to_request_string = ""
   for i in range(len(array)-1):
      equipments_to_request_string += ''.join([name for name in globals() if globals()[name] is array[i]]) + ","
   equipments_to_request_string += ''.join([name for name in globals() if globals()[name] is array[len(array)-1]])
   return equipments_to_request_string
