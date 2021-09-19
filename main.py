from fastapi import FastAPI, HTTPException
from models.users_container import Users_container
from models.user import User
from models.request import Request

app = FastAPI()

users = Users_container()


@app.get("/")
async def root():
    return {"message": "You are using your purchases tracker"}


@app.get("/add_user")
async def add_user():
    users.add_user(User())


@app.get("/all_users")
async def get_users_amount():
    return users.users_amount()


@app.get("/users/{user_id}/items")
async def get_items_amount(user_id: int):
    if user_id >= users.users_amount():
        raise HTTPException(status_code=404, detail="User not found")
    return users.get_user(user_id).get_items_amount()


@app.post("users/{user_id}/items/add")
async def add_item(user_id: int, request: Request):
    if user_id >= users.users_amount():
        raise HTTPException(status_code=404, detail="User not found")
    if request.item_amount <= 0:
        raise HTTPException(status_code=404, detail="You need to add at least one item")
    if request.price_for_one_item < 0:
        raise HTTPException(status_code=404, detail="Item price can not be negative")
    users.get_user(user_id).add_item_from_request(request)
    return "Added items price:" + str(request.item_amount * request.price_for_one_item)
