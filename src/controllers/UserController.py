from ..config.Conection import Conection
from ..database.User_schema import User
from passlib.context import CryptContext


encriptador = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def hash_password(password: str) -> str:
    return encriptador.hash(password)

async def create_user(username: str, password: str, role_id: int):
    password_hash = hash_password(password)

    db = Conection()

    try:

        result = await db.execute(
            "INSERT INTO users (username, password_hash, role_id) VALUES (?,?,?)",
            [username,password_hash,role_id]
        )

        if result.rows_affected == 0:
            return None

        return {"message": "Usuario creado exitosamente", "username": username}
    
    except Exception:
        raise

async def get_users() -> list[User]:
    
    db =Conection()
    

    result = await db.execute(
        "SELECT * FROM users"
    )

    #Se usa esta lista cuando hay mas de una fila de datos que se consulta (lista dde diccionarios)
    user_list =[ User(**dict(zip(result.columns, row)))
           for row in result.rows]
        
    return user_list
    

async def get_users_by_id(user_id: int) -> User:    
    db = Conection()

    result = await db.execute(
        f"SELECT * FROM users WHERE id =?",
        [user_id]
        
    )

    if not result.rows:
        return None

    #Se usa esta  cuando hay una sola fila de datos que se consulta (un solo diccionario directamente)
    user_dict = dict(zip(result.columns, result.rows[0]))
           
    
    return User(**user_dict)



async def update_user(user_id: int, username: str, role_id: int) -> bool:
    db = Conection()
    
    result = await db.execute(
        "UPDATE users SET username = ?, role_id = ? WHERE id = ?",
        [username, role_id, user_id]
    )
    
    return True
    
async def delete_user(user_id: int):
    db = Conection()

    result = await db.execute(
        "DELETE FROM users WHERE ID = ? ",
        [user_id]
    )

    return True
    






    
    