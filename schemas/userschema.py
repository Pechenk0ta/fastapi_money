from pydantic import BaseModel
from typing import Union

class userCreateSchema(BaseModel):
    username: str
    password: str
    email: str

class userByIdSchema(BaseModel):
    id: int


class userChangeData(BaseModel):
    id : int
    username : Union[str, None]
    email : Union[str, None]

