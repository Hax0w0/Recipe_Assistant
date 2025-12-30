from typing import List

from Infrastructure.strawberry_mappings import *

from Infrastructure.Utils.llm_utils import LLM_Utils
from Infrastructure.Utils.database_utils import Database_Utils

class Recipe_Service:

    def __init__(self, database: Database_Utils, llm: LLM_Utils):
        self.database = database
        self.llm = llm

    def get_all(self) -> List[Recipe]:
        
        # Get the list of recipes from the database
        recipe_list = self.database.get_all_recipes()

        # Convert to Strawberry types
        recipes = list()
        for recipe in recipe_list:
            recipe_type = recipe_type_mapping(recipe)
            recipes.append(recipe_type)

        return recipes

    def get_by_name(self, name: str) -> Recipe_Type:

        # Get the recipe by name from the database
        recipe_info = self.database.get_recipe_by_name(name)
        recipe = recipe_type_mapping(recipe_info)

        return recipe

    def summarize(self, name: str) -> str:

        recipe = self.database.get_recipe_by_name(name)
        return self.llm.summarize_recipe(recipe)

    def rate(self, name: str) -> str:
        
        recipe = self.database.get_recipe_by_name(name)
        return self.llm.rate_recipe(recipe)
