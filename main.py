from fastapi import FastAPI, HTTPException
from models.users_container import Users_container
from models.user import User
from models.request import Request
from starlette import status
from starlette.responses import Response

app = FastAPI()


class PurchasesManager():

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
async def get_item(user_id: int, item_name: str):
    manager.check_user_id(user_id)
    return manager.users.get_user(user_id).get_item(item_name)
