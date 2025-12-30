import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from GraphQL.query import Query

app = FastAPI(title="Recipe Assistant")

# Create Strawberry GraphQL router
schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schema, path="/graphql", graphiql=True)

# Mount GraphQL on FastAPI
app.include_router(graphql_app)

@app.get("/test")
async def test():
    return {"ok": True}