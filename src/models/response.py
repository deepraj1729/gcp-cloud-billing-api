from pydantic import BaseModel
from typing import Optional

class ResponseModel(BaseModel):
    data:list | dict = {}
    errors: Optional[str] = []
    message: Optional[str] = ""
    status: int = 200