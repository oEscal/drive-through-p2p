# messages's methods
NODE_JOIN = 0
NODE_DISCOVERY = 1
ORDER = 2
PICKUP = 3
TOKEN = 4
TICKET = 5

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
