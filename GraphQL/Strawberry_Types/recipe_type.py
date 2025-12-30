import strawberry
from typing import List, Optional

from .step_type import Step_Type
from .nutrition_type import Nutrition_Type
from .ingredient_type import Ingredient_Type

@strawberry.type
class Recipe_Type:
    name: str
    ingredients: List[Ingredient_Type]
    steps: List[Step_Type]
    nutrition_facts: Nutrition_Type
