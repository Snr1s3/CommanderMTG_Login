from typing import Optional
from pydantic import BaseModel, Field


class Usuari(BaseModel):
    id: int = Field(..., description="Unique identifier for the user")
    name: str = Field(..., description="User's display name")
    mail: str = Field(..., description="User's email address")
    hash: str = Field(..., description="Hashed password")

class CreateUsuari(BaseModel):
    name: str = Field(..., description="User's display name (3-50 characters)")
    mail: str = Field(..., description="Valid email address")
    hash: str = Field(..., description="Password hash (minimum 8 characters)")

class AuthRequest(BaseModel):
    name: str = Field(..., description="User's display name (3-50 characters)")
    hash: str = Field(..., description="Password hash (minimum 8 characters)")

class UpdateUsuariComplete(BaseModel):
    name: Optional[str] = Field(None, description="User's display name (3-50 characters)")
    mail: Optional[str] = Field(None, description="Valid email address")
    hash: str = Field(..., description="Password hash (minimum 8 characters)")