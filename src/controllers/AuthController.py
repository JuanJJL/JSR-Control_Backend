# controlador = crear token, enviar login, registro *recuperar contra 
import os
from ..config.Conection import Conection
from passlib.context import CryptContext
import jwt
from dotenv import load_dotenv
from ..database.User_schema import UserRead as UserData

load_dotenv()
db = Conection()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
TOKEN_LIFESPAN = 300

encriptador = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def hash_password(password: str) -> str:
    return encriptador.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    try:
        # Usa el método verify de passlib para comparar el hash almacenado
        return encriptador.verify(password, hashed_password)
    except Exception:
        # Esto captura errores si el hash almacenado es inválido o el formato es incorrecto
        return False

def create_token(user: UserData) -> str:
    info = {
        "user_id": user.id,
        "username": user.username,
        "role_id": user.role_id,
        "status": user.status,
    }
    
    token = jwt.encode(info, SECRET_KEY, algorithm=ALGORITHM)
    return token



async def check_credentials(username: str, password: str):
    db = None 
    try:
        db = Conection()

        result = await db.execute(
            "SELECT id, username, password_hash, status, role_id, created_at, updated_at FROM users WHERE username = ? ",
            [username]
        )

        if not result.rows:
            return None
        
        # El mapeo a user_data por nombre de columna es correcto, pero debe coincidir con el SELECT.
        user_data = dict(zip(result.columns, result.rows[0]))

        # Aquí falla si 'password_hash' no se recuperó o el valor es incorrecto.
        if not verify_password(password, user_data["password_hash"]):
            return None
        
        return user_data # Esto es lo que se usa para crear el token
    
    except Exception as e:
        raise e 
    finally:
        if db:
            await db.close()


    

    





        










