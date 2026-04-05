# schema de validação do user
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CreateUser(BaseModel):
    """Classe usada para validar a criação do usuário via POST"""
    id: int = Field(...)
    name: str = Field(..., max_length=100)
    email: EmailStr = Field(..., max_length=150)
    password: str = Field(..., max_length=255)
    model_config = ConfigDict(from_attributes=True)


class GetUser(BaseModel):
    name: str
    email: EmailStr
