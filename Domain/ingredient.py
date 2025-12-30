from typing import Optional

class Ingredient:
    name: str
    quantity: float
    unit: str

    def __init__(self, name: str, quantity: float, unit: str):
        
        self.name = name
        self.quantity = quantity
        self.unit = unit