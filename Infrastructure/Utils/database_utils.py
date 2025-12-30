import os
import sqlite3
from typing import List

from Domain.step import Step
from Domain.recipe import Recipe
from Domain.nutrition import Nutrition
from Domain.ingredient import Ingredient

class Database_Utils:

    def connect_to_database(self) -> sqlite3.Connection:

        # Create a local database file and connect to it
        path = os.path.join(os.path.dirname(__file__),
                            "..", "..", "Database", "Recipes.db")
        database = sqlite3.connect(path)

        # Make SQLite return rows as dictionary-like objects
        database.row_factory = sqlite3.Row

        return database
    
    def get_all_recipes(self) -> List[Recipe]:

        # Connect to the database
        database = self.connect_to_database()
        cursor = database.cursor()

        # Get all recipe names
        cursor.execute("SELECT name FROM recipes")
        recipe_names = [recipe["name"] for recipe in cursor.fetchall()]

        # Close the database connection
        database.close()

        # Build a list of Recipe objects
        recipes = list()
        for name in recipe_names:
            recipe = self.get_recipe_by_name(name)
            recipes.append(recipe)

        return recipes
    
    def get_recipe_by_name(self, recipe_name: str) -> Recipe:

        # Connect to the database
        database = self.connect_to_database()
        cursor = database.cursor()

        # Try to get the recipe by name
        cursor.execute("SELECT * FROM recipes WHERE name=?", (recipe_name,))
        recipe_info = cursor.fetchone()

        # Raise an error if the recipe does not exist
        if recipe_info is None:
            raise ValueError(f"Recipe '{recipe_name}' not found")
        else:
            recipe_ID, name, calories, fat, carbs, protein = recipe_info
            nutrition = Nutrition(calories=calories,
                                  fat=fat,
                                  carbs=carbs,
                                  protein=protein)

        # Get the ingredients and steps for the recipe
        ingredients = self.get_ingredients_for_recipe(recipe_ID)
        steps = self.get_steps_for_recipe(recipe_ID)

        # Close the database connection
        database.close()

        # Create and return the Recipe object
        recipe = Recipe(name=name,
                        ingredients=ingredients,
                        steps=steps,
                        nutrition_facts=nutrition)
        
        return recipe
        
    def get_ingredients_for_recipe(self, recipe_ID: int) -> List[Ingredient]:

        # Connect to the database
        database = self.connect_to_database()
        cursor = database.cursor()

        # Get the ingredients for the recipe
        cursor.execute("SELECT * FROM ingredients WHERE recipe_ID=?",
                       (recipe_ID,))
        
        # Build the list of Ingredient objects
        ingredients = list()
        for ingredient_row in cursor.fetchall():
            ingredient = Ingredient(name=ingredient_row["name"],
                                    quantity=ingredient_row["quantity"],
                                    unit=ingredient_row["unit"])
            ingredients.append(ingredient)

        return ingredients
    
    def get_steps_for_recipe(self, recipe_ID: int) -> List[Step]:

        # Connect to the database
        database = self.connect_to_database()
        cursor = database.cursor()

        # Get the steps for the recipe
        cursor.execute("SELECT * FROM steps WHERE recipe_ID=?",
                       (recipe_ID,))
        
        # Build the list of Step objects
        steps = list()
        for step_row in cursor.fetchall():
            step = Step(number=step_row["step_number"],
                        description=step_row["instruction"])
            steps.append(step)

        return steps
    