from typing import List

from Domain.step import Step
from Domain.recipe import Recipe
from Domain.nutrition import Nutrition
from Domain.ingredient import Ingredient

from GraphQL.Strawberry_Types.step_type import Step_Type
from GraphQL.Strawberry_Types.recipe_type import Recipe_Type
from GraphQL.Strawberry_Types.nutrition_type import Nutrition_Type
from GraphQL.Strawberry_Types.ingredient_type import Ingredient_Type

def step_type_mapping(step: Step) -> Step_Type:

    step_type = Step_Type(number=step.number,
                          description=step.description)
    
    return step_type

def nutrition_type_mapping(nutrition: Nutrition) -> Nutrition_Type:

    nutrition_type = Nutrition_Type(calories=nutrition.calories,
                                    fat=nutrition.fat,
                                    carbs=nutrition.carbs,
                                    protein=nutrition.protein)
    
    return nutrition_type

def ingredient_type_mapping(ingredient: Ingredient) -> Ingredient_Type:
    
    ingredient_type = Ingredient_Type(name=ingredient.name,
                                      quantity=ingredient.quantity,
                                      unit=ingredient.unit)
    
    return ingredient_type

def recipe_type_mapping(recipe: Recipe) -> Recipe_Type:

    ingredient_types = list()
    for ingredient in recipe.ingredients:
        ingredient_type = ingredient_type_mapping(ingredient)
        ingredient_types.append(ingredient_type)

    step_types = list()
    for step in recipe.steps:
        step_type = step_type_mapping(step)
        step_types.append(step_type)

    nutrition_type = nutrition_type_mapping(recipe.nutrition_facts)

    recipe_type = Recipe_Type(name=recipe.name,
                              ingredients=ingredient_types,
                              steps=step_types,
                              nutrition_facts=nutrition_type)
    
    return recipe_type