import strawberry
from typing import Optional

@strawberry.type
class Ingredient_Type:
    name: str
    quantity: Optional[float]
    unit: Optional[str]