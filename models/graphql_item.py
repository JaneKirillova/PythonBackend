from graphene import String, Float, Int, ObjectType


class GraphQLItem(ObjectType):
    name = String(required=True)
    price = Float(required=True)
    amount = Int(required=True)

