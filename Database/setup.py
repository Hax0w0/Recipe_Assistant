import os
import json
import sqlite3

def initialize_database():

    # Connect to SQLite database (or create it if it doesn't exist)
    path = os.path.join(os.path.dirname(__file__), "Recipes.db")
    database = sqlite3.connect(path)
    cursor = database.cursor()

    # Define the table schemas
    recipe_columns = """
        recipe_ID    INTEGER PRIMARY KEY AUTOINCREMENT,
        name         TEXT NOT NULL,
        calories     INTEGER NOT NULL,
        fat          INTEGER NOT NULL,
        carbs        INTEGER NOT NULL,
        protein      INTEGER NOT NULL
        """

    ingredient_columns = """
        recipe_ID       INTEGER NOT NULL,
        name            TEXT NOT NULL,
        quantity        TEXT NOT NULL,
        unit            TEXT NOT NULL,
        FOREIGN KEY (recipe_id) REFERENCES recipes(id)
        """
    
    steps_columns = """
        recipe_ID      INTEGER NOT NULL,
        step_number    INTEGER NOT NULL,
        instruction    TEXT NOT NULL,
        FOREIGN KEY (recipe_id) REFERENCES recipes(id)
    """

    # Create the tables
    cursor.execute(f"CREATE TABLE IF NOT EXISTS recipes ({recipe_columns})")
    cursor.execute(f"CREATE TABLE IF NOT EXISTS ingredients ({ingredient_columns})")
    cursor.execute(f"CREATE TABLE IF NOT EXISTS steps ({steps_columns})")

    # Commit changes and close the connection
    database.commit()
    database.close()

def populate_database():

    # Connect to SQLite database
    path = os.path.join(os.path.dirname(__file__), "Recipes.db")
    database = sqlite3.connect(path)
    cursor = database.cursor()

    # Load the JSON file
    data_path = os.path.join(os.path.dirname(__file__),
                             "..", "Data_Files", "Recipes.JSON")
    with open(data_path, "r") as file:
        recipes = json.load(file)

    # Insert each recipe into the database
    for recipe in recipes:
        recipe_ID = insert_recipe(recipe, cursor)

        # Insert each ingredient for the recipe
        for ingredient in recipe["ingredients"]:
            insert_ingredient(recipe_ID, ingredient, cursor)

        # Insert each step for the recipe
        for step_number, instruction in recipe["steps"].items():
            insert_step(recipe_ID, step_number, instruction, cursor)

    # Commit changes and close the connection
    database.commit()
    database.close()

def insert_recipe(recipe, cursor):

    # Get the recipe details
    name = recipe["name"]
    calories = recipe["nutrition_facts"]["calories"]
    fat = recipe["nutrition_facts"]["fat"]
    carbs = recipe["nutrition_facts"]["carbs"]
    protein = recipe["nutrition_facts"]["protein"]

    # Insert information into recipe table
    cursor.execute(f"""INSERT INTO recipes
                    (name, calories, fat, carbs, protein)
                    VALUES (?, ?, ?, ?, ?)""",
                    (name, calories, fat, carbs, protein))
    
    # Return the recipe ID
    recipe_ID = cursor.lastrowid

    return recipe_ID

def insert_ingredient(recipe_ID, ingredient, cursor):

    # Get the quantity and unit of the ingredient
    name = ingredient["name"]
    quantity = ingredient["quantity"]
    unit = ingredient["unit"]

    # Insert into recipe_ingredients table
    cursor.execute(f"""INSERT INTO ingredients
                   (recipe_ID, name, quantity, unit)
                   VALUES (?, ?, ?, ?)""",
                   (recipe_ID, name, quantity, unit))

def insert_step(recipe_ID, step_number, instruction, cursor):

    # Insert into steps table
    cursor.execute(f"""INSERT INTO steps
                    (recipe_ID, step_number, instruction)
                    VALUES (?, ?, ?)""",
                    (recipe_ID, step_number, instruction))

if __name__ == "__main__":
    initialize_database()
    populate_database()