import time
import random
from utils import GRILL_MEAN, GRILL_STD, FRIDGE_MEAN, FRIDGE_STD, FRYER_MEAN, FRYER_STD, REQUEST_GRILLER, REQUEST_FRIDGE, REQUEST_FRYER

class KitchenEquipment:
   def __init__(self, mean, std,number ):
      self.mean = mean
      self.std = std
      self.request_number = number

   def cook(self, number):
      for i in range(number):
         time.sleep(random.gauss(self.mean, self.std))


class Grill(KitchenEquipment):
   def __init__(self):
      super().__init__(GRILL_MEAN, GRILL_STD,REQUEST_GRILLER)

class Fridge(KitchenEquipment):
   def __init__(self):
      super().__init__(FRIDGE_MEAN, FRIDGE_STD,REQUEST_FRIDGE)

class Fryer(KitchenEquipment):
   def __init__(self):
      super().__init__(FRYER_MEAN, FRYER_STD,REQUEST_FRYER)