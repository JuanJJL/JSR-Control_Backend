# controlador = crear token, enviar login, registro *recuperar contra 
import os
from ..config.Conection import Conection
from passlib.context import CryptContext
from passlib.hash import pbkdf2_sha256
import jwt
from dotenv import load_dotenv
from datetime import datetime, timedelta

from ..database.User_schema import User

load_dotenv()
db = Conection()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
TOKEN_LIFESPAN = 300



def hash_password(password: str) -> str:
    return pbkdf2_sha256.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return pbkdf2_sha256.verify(password, hashed_password)

def create_token(user: User) -> str:
    expiration = datetime.utcnow() + timedelta(minutes=TOKEN_LIFESPAN)

    info = {
        "user_id": user.id,
        "username": user.username,
        "role_id": user.role_id,
        "status": user.status,
        "exp": expiration.timestamp()
    }
    
    token = jwt.encode(info, SECRET_KEY, algorithm=ALGORITHM)
    return token



async def check_credentials(username: str, password: str)-> User | None:
    result = await db.execute(
        "SELECT * FROM users WHERE username = ? ",
        [username]
    )

    if not result.rows:
        return None
    
    user_dict = dict(zip(result.columns, result.rows[0]))

    if not verify_password(password, user_dict["password_hash"]):
        return None
    
    return User(**user_dict)
    


    

    





        










