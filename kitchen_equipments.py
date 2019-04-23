import time
import random

# equipment variables
GRILL_MEAN = 3
GRILL_STD = 0.5
FRIDGE_MEAN = 1
FRIDGE_STD = 0.5
FRYER_MEAN = 5
FRYER_STD = 0.5
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
