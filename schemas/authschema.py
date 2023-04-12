from pydantic import BaseModel


class userLogin(BaseModel):
    username: str
    password: str
