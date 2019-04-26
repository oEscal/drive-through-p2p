# messages's methods
NODE_JOIN = 0
REQUEST_INFO = 1
NODE_DISCOVERY = 2
ORDER = 3
PICKUP = 4
TOKEN = 5
TICKET = 6
GIVE_FOOD = 7
KEEP_ALIVE = 8
IM_ALIVE = 9
CLEAR_TABLE = 10

# request equipment
REQUEST_GRILL = 0
REQUEST_FRIDGE = 1
REQUEST_FRYER = 2

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


def print_out(input_str):
   string_order = ""
   for i in range(len(input_str) - 1):
      string_order += str(input_str[i]) + ", "
   string_order += str(input_str[len(input_str) - 1])
   return string_order
