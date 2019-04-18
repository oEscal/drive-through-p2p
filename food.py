from kitchen_equipments import Grill, Fridge, Fryer

class Food:
   def __init__(self, name, number, equipment_required_to_cook):
      self.name = name
      self.number = number
      self.equipment_required_to_cook = equipment_required_to_cook

class Hamburger(Food):
   name = "hamburger"

   def __init__(self, number):
      super().__init__(Hamburger.name, number, Grill())

class Drink(Food):
   name = "drink"

   def __init__(self, number):
      super().__init__("drink", number, Fridge())

class Chips(Food):
   name = "chips"

   def __init__(self, number):
      super().__init__("chips", number, Fryer())
