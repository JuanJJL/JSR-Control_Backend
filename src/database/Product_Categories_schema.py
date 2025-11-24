from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Modelo de entrada para crear una categoría (POST)
class ProductCategoryCreate(BaseModel):
    category: str

# Modelo de lectura (salida) (GET)
class Product_Category(BaseModel):
    id: int
    category: str
    created_at: str 
    updated_at: str

    class Config:
        from_attributes = True