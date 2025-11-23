from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Modelo base para creación y actualización (sin ID) (POST)
class UserCreate(BaseModel):
    username: str
    password: str 
    role_id: int
#  Modelo de lectura y escritura (incluye ID) (get y put)
class UserRead(BaseModel):
    id: int
    username: str
    role_id: int
    status: int = 1
    created_at: str 
    updated_at: str
    
    class Config:
        from_attributes = True

# Modelo de actualizacion (Todos los campos son opcionales)
class UserUpdate(BaseModel):
    username: Optional[str] = None
    role_id: Optional[int] = None