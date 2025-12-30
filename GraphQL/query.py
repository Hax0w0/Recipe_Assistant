import strawberry
from typing import List

from Domain.recipe import Recipe

from GraphQL.Strawberry_Types.recipe_type import Recipe_Type

from Infrastructure.recipe_service import Recipe_Service

from Infrastructure.Utils.llm_utils import LLM_Utils
from Infrastructure.Utils.database_utils import Database_Utils

@strawberry.type
class Query:

    service = Recipe_Service(Database_Utils(), LLM_Utils())

    @strawberry.field
    def display_all_recipes(self) -> List[Recipe_Type]:
        return Query.service.get_all()
    
    @strawberry.field
    def display_recipe_by_name(self, name: str) -> Recipe_Type:
        return Query.service.get_by_name(name)

    @strawberry.field
    def summarize_recipe(self, name: str) -> str:
        return Query.service.summarize(name)

    @ strawberry.field
    def rate_recipe(self, name: str) -> str:
        return Query.service.rate(name)

