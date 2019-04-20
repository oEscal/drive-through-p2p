import time
import random
from utils import GRILL_MEAN, GRILL_STD, FRIDGE_MEAN, FRIDGE_STD, FRYER_MEAN, FRYER_STD

class KitchenEquipment:
   def __init__(self, mean, std):
      self.mean = mean
      self.std = std

   def cook(self, number):
      for i in range(number):
         time.sleep(abs(random.gauss(self.mean, self.std)))
   def __str__(self):
      return self.__class__.__name__


class Grill(KitchenEquipment):
   def __init__(self):
      super().__init__(GRILL_MEAN, GRILL_STD)

class Fridge(KitchenEquipment):
   def __init__(self):
      super().__init__(FRIDGE_MEAN, FRIDGE_STD)

class Fryer(KitchenEquipment):
   def __init__(self):
      super().__init__(FRYER_MEAN, FRYER_STD)
