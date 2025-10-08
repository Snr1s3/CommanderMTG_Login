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

class UpdateUsuariName(BaseModel):
    name: str = Field(..., description="User's display name (3-50 characters)")

class UpdateUsuariMail(BaseModel):
    mail: str = Field(..., description="Valid email address")

class UpdateUsuariPassword(BaseModel):
    
    hash: str = Field(..., description="Password hash (minimum 8 characters)")