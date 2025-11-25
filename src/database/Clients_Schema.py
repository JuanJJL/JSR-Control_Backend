from pydantic import BaseModel, EmailStr
from typing import Optional

# Modelo de entrada (POST)
class ClientCreate(BaseModel):
    name: str
    email: EmailStr
    age: int
    details: Optional[str] = None

# Modelo para actualizar un cliente (PUT)
class ClientUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    age: Optional[int] = None
    details: Optional[str] = None

# Modelo para leer (GET)
class Client(BaseModel):
    id: int
    name: str
    email: str
    age: int
    details: Optional[str]
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True

