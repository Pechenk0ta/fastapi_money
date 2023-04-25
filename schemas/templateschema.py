from pydantic import BaseModel
from typing import Union

class templateschema(BaseModel):
    name : str
    description : str
    value : int
    category : str
