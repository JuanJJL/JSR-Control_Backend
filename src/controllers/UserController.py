from ..config.Conection import Conection
from ..database.User_schema import User
from ..controllers.AuthController import hash_password

async def get_user_by_username(username):
    db = Conection()


    result = await db.execute(
        "SELECT username from users where username = ? ",
        [username]
    )

    if not result.rows:
        return None
    

    return result.rows[0][0]


    



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
    except Exception as e:
        return {"message": f"{e}"}

async def get_users() -> list[User]:
    
    db =Conection()
    
    try:
        result = await db.execute(
            "SELECT * FROM users"
        )

        db.close

        user_list =[ User(**dict(zip(result.columns, row)))
            for row in result.rows]
            
        return user_list
    
    except Exception as e:
        return {"message": f"{e}"}
    
        
    

async def get_users_by_id(user_id: int) -> User:    
    db = Conection()

    try:
        result = await db.execute(
            f"SELECT * FROM users WHERE id =?",
            [user_id]    
        )

        db.close

        if not result.rows:
            return None

        
        user_dict = dict(zip(result.columns, result.rows[0]))
            
        
        return User(**user_dict)
    except Exception as e:
        return {"message": f"{e}"}




async def update_user(user_id: int, username: str, role_id: int) -> bool:
    db = Conection()
    
    try:

        result = await db.execute(
            "UPDATE users SET username = ?, role_id = ? WHERE id = ?",
            [username, role_id, user_id]
        )

        db.close
        
        return True
    except Exception as e:
        db.close
        return {"message": f"{e}"}

    
#Cambiar a Desactivar usuario

async def deactivate_user(user_id: int):
    db = Conection()

    result = await db.execute(
        "DELETE FROM users WHERE ID = ?",
        [user_id]
    )


    db.close



    return True
    






    
    