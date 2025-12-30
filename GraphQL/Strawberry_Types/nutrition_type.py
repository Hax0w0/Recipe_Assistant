import strawberry

@strawberry.type
class Nutrition_Type:
    calories: int
    fat: int
    carbs: int
    protein: int