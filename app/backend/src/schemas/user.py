# schema de validação do user
from pydantic import BaseModel, ConfigDict, EmailStr

class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    password: str
    model_config = ConfigDict(from_attributes=True)