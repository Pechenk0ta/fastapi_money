from pydantic import BaseModel


class userCreateSchema(BaseModel):
    username: str
    password: str
    email: str

class userByIdSchema(BaseModel):
    id: int