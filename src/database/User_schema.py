
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class User(BaseModel):
    id: int
    username: str
    password_hash: str
    role_id: int
    created_at: str 
    updated_at: str

class UserUpdate(BaseModel):
    username: str
    role_id: int
