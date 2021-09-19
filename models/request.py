from typing import Optional

from pydantic import BaseModel


class Request(BaseModel):
    item_name: Optional[str]
    price_for_one_item: Optional[float]
    item_amount: Optional[int]
