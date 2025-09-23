from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


class User(BaseModel):
    id : int
    name : str
    mail : str
    pwd : str


class AuthRequest(BaseModel):
    name: str
    pwd: str

class UpdateRequest(BaseModel):
    id: int
    name: Optional[str] = None
    mail: Optional[str] = None
    pwd: Optional[str] = None