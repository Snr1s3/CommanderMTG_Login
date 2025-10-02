from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


class Usuari(BaseModel):
    id : int
    name : str
    mail : str
    hash : str

class CreateUsuari(BaseModel):
    name : str
    mail : str
    hash : str

class UpdateUsuari(BaseModel):
    id: int
    name: Optional[str] = None
    mail: Optional[str] = None
    hash: Optional[str] = None
class AuthRequest(BaseModel):
    name: str
    hash: str
