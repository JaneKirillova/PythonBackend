import graphene
from fastapi import FastAPI, HTTPException
import graphql
from starlette import status
from starlette.graphql import GraphQLApp
from starlette.responses import Response

from models.graphql_user import *
from models.one_item import Item
from models.request import Request
from models.user import User
from models.users_container import Users_container

app = FastAPI()


class PurchasesManager:

    def __init__(self):
        self.users = Users_container()

    def check_user_id(self, user_id):
        if user_id >= self.users.users_amount():
            raise HTTPException(status_code=404, detail="User not found")

    def clear_base(self):
        self.users = Users_container()

    def check_item_amount(self, item_amount):
        if item_amount > 0:
            return
        raise HTTPException(status_code=404, detail="You need to add at least one item")

    def check_price_for_one_item(self, price_for_one_item):
        if price_for_one_item >= 0:
            return
        raise HTTPException(status_code=404, detail="Item price can not be negative")

    def make_answer_for_request(self, request: Request) -> str:
        return "Added items price: " + str(request.item_amount * request.price_for_one_item)


manager = PurchasesManager()


@app.get("/")
async def root():
    return Response("You are using your purchases tracker", status_code=status.HTTP_200_OK)


@app.get("/clear_base")
async def clear():
    manager.clear_base()
    return Response("Base was cleared", status_code=status.HTTP_200_OK)


@app.get("/add_user")
async def add_user():
    manager.users.add_user(User())
    return Response("User successfully added", status_code=status.HTTP_200_OK)


@app.get("/users_amount")
async def get_users_amount():
    return manager.users.users_amount()


@app.get("/items_amount/{user_id}")
async def get_items_amount(user_id: int):
    manager.check_user_id(user_id)
    return manager.users.get_user(user_id).get_different_items_amount()


@app.post("/add")
async def add(request: Request):
    return Response(manager.make_answer_for_request(request), status_code=status.HTTP_200_OK)


@app.post("/add_item/{user_id}")
async def add_item(user_id: int, request: Request):
    manager.check_user_id(user_id)
    manager.check_item_amount(request.item_amount)
    manager.check_price_for_one_item(request.price_for_one_item)
    manager.users.get_user(user_id).add_item_from_request(request)
    return Response(manager.make_answer_for_request(request), status_code=status.HTTP_200_OK)


@app.get("/get_item/{user_id}/{item_name}")
async def get_item(user_id: int, item_name: str) -> Item:
    manager.check_user_id(user_id)
    return manager.users.get_user(user_id).get_item(item_name)


class Query(graphene.ObjectType):
    item = Field(GraphQLItem, user_id=Int(), name=String())
    user = Field(GraphQlUser, user_id=Int())
    users = List(GraphQlUser)

    def resolve_users(self, info):
        users_to_return = list()
        for user_id, user in enumerate(manager.users.users):
            items_to_ret = list()
            for i in user.items:
                items_to_ret.append(GraphQLItem(user.items[i].name, user.items[i].price, user.items[i].amount))
            users_to_return.append(GraphQlUser(user_id, "user" + str(user_id), items_to_ret))
        return users_to_return

    def resolve_user(self, info, user_id):
        if user_id >= manager.users.users_amount():
            raise graphql.GraphQLError("There is no user with this id " + str(user_id))
        user = manager.users.get_user(user_id)
        items_to_ret = list()
        for i in user.items:
            items_to_ret.append(GraphQLItem(user.items[i].name, user.items[i].price, user.items[i].amount))
        return GraphQlUser(user_id, "user" + str(user_id), items_to_ret)

    def resolve_item(self, info, user_id, name):
        if user_id >= manager.users.users_amount():
            raise graphql.GraphQLError("There is no user with this id " + str(user_id))
        user = manager.users.get_user(user_id)
        try:
            item = user.get_item(name)
            return GraphQLItem(name=item.name, price=item.price, amount=item.amount)
        except Exception:
            raise graphql.GraphQLError("there is no item with name " + name)


app.add_route("/graphql", GraphQLApp(schema=graphene.Schema(query=Query)))
