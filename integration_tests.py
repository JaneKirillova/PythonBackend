import pytest
from models.request import Request
from fastapi import HTTPException
import main


@pytest.mark.asyncio
async def test_integration_add_users_and_clear():
    response_root = await main.root()
    assert response_root.status_code == 200
    assert response_root.body == b"You are using your purchases tracker"

    response_add = await main.add_user()
    assert response_add.status_code == 200
    assert response_add.body == b"User successfully added"

    await main.add_user()
    response_users_amount = await main.get_users_amount()
    assert response_users_amount == 2

    response_clear = await main.clear()
    assert response_clear.status_code == 200
    assert response_clear.body == b"Base was cleared"


@pytest.mark.asyncio
async def test_integration_add_item():
    await main.add_user()
    request = Request(item_name="carrot", price_for_one_item=10, item_amount=2)
    response_add_item = await main.add_item(0, request)
    assert response_add_item.status_code == 200
    assert response_add_item.body == b"Added items price: 20.0"

    response_get_item = await main.get_item(0, "carrot")
    assert response_get_item.name == "carrot"
    assert response_get_item.amount == 2
    assert response_get_item.price == 10

    response_items_amount = await main.get_items_amount(0)
    assert response_items_amount == 1


@pytest.mark.asyncio
async def test_integration_bad_requests():
    await main.add_user()
    with pytest.raises(HTTPException):
        await main.get_items_amount(10)

    bad_request = Request(item_name="carrot", price_for_one_item=-10, item_amount=2)

    with pytest.raises(HTTPException):
        await main.add_item(0, bad_request)
