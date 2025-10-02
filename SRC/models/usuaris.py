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


class AuthRequest(BaseModel):
    name: str
    hash: str

class UpdateUsuariName(BaseModel):
    name: str

class UpdateUsuariMail(BaseModel):
    mail: str

class UpdateUsuariPassword(BaseModel):
    hash: str