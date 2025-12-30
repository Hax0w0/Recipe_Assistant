import os
from dotenv import load_dotenv

from typing import List

from Domain.step import Step
from Domain.nutrition import Nutrition
from Domain.ingredient import Ingredient

class Recipe:
    name: str
    ingredients: List[Ingredient]
    steps: List[Step]
    nutrition_facts: Nutrition

    def __init__(self, name, ingredients, steps, nutrition_facts):
        
        self.name = name
        self.ingredients = ingredients
        self.steps = steps
        self.nutrition_facts = nutrition_facts

    def get_summary_prompt(self) -> str:

        prompt = f"""
            Summarize the following recipe in 2–3 sentences.
            Recipe name: {self.name}
            Ingredients: {self.ingredients}
            Steps: {self.steps}
            """
        
        return prompt
    
    def get_rating_prompt(self) -> str:

        prompt = f"""
            In 2-3 sentences, can you say what kinds of diets, goals, etc. this recipe is good for?
            Recipe name: {self.name}
            Ingredients: {self.ingredients}
            Nutrition Facts: {self.nutrition_facts}
            """
        
        return prompt
