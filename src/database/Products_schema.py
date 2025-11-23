from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Modelo de entrada para crear un producto (POST)
class ProductCreate(BaseModel):
    name: str
    price: int
    cost: int
    stock: int
    category_id: int

# Modelo para actualizar (todos los campos son opcionales) (PUT)
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[int] = None
    cost: Optional[int] = None
    stock: Optional[int] = None
    category_id: Optional[int] = None

# Modelo de lectura (salida) (GET)
class Product(BaseModel):
    id: int
    name: str
    price: int
    cost: int
    stock: int
    category_id: int
    created_at: str 
    updated_at: str
    
    class Config:
        from_attributes = True