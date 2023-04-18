from pydantic import BaseModel
from typing import Union

class moneycreateschema(BaseModel):
    value : int
    description : Union[str, None]
    type : str


class money_changes(BaseModel):
    day_start :Union[str, None]
    day_end: Union[str, None]
