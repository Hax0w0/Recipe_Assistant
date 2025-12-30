class Nutrition:
    calories: int
    fat: int
    carbs: int
    protein: int

    def __init__(self, calories: int, fat: int, carbs: int, protein: int):
        
        self.calories = calories
        self.fat = fat
        self.carbs = carbs
        self.protein = protein