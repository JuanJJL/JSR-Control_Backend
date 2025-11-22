# controlador = crear token, enviar login, registro *recuperar contra 
import os
from ..config.Conection import Conection
from passlib.context import CryptContext
import jwt
from dotenv import load_dotenv
from datetime import datetime, timedelta
import hashlib
from ..database.User_schema import User

load_dotenv()
db = Conection()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
TOKEN_LIFESPAN = 300

encriptador = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def hash_password(password: str) -> str:
    return encriptador.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return hash_password(password) == hashed_password

def create_token(user: User) -> str:
    info = {
        "user_id": user.id,
        "username": user.username,
        "role_id": user.role_id,
        "status": user.status,
        "expiration": datetime.utcnow() + timedelta(minutes = TOKEN_LIFESPAN)
    }
    
    token = jwt.encode(info, SECRET_KEY, algorithm=ALGORITHM)
    return token



async def check_credentials(username: str, password: str):
    result = await db.execute(
        "SELECT id, username, password_hash, role_id FROM users WHERE username = ? ",
        [username]
    )

    if not result.rows:
        return None
    
    user_data = dict(zip(result.columns, result.rows[0]))

    if not verify_password(password, user_data["password_hash"]):
        return None
    
    return user_data
    


    

    





        










