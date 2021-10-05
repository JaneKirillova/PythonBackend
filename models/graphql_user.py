from graphene import String, Int, Field, List, ObjectType
from models.graphql_item import GraphQLItem


class GraphQlUser(ObjectType):
    id = Int(required=True)
    user_name = String(required=True)
    items = Field(List(GraphQLItem))
