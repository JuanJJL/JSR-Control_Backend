from typing import Optional
from ..config.Conection import Conection
from ..database.User_schema import UserRead
from ..controllers.AuthController import hash_password


async def create_user(username: str, password: str, role_id: int):
    
    password_hash = hash_password(password)
    db = Conection()
    try: 
        # 1. INSERTAR: Usamos los nombres de columna correctos (username, role_id)
        insert_result = await db.execute(
            "INSERT INTO users (username, password_hash, role_id) VALUES (?,?,?)",
            [username, password_hash, role_id]
        )

        # 2. OBTENER ID (Asumimos que el cierre de conexión está en un 'finally' global)
        new_id = insert_result.last_insert_rowid 
        if new_id is None:
             raise Exception("La base de datos no devolvió el ID del nuevo usuario.")

        # 3. RECUPERAR: Usamos ALIAS para mapear de DB a Pydantic (name AS username, id_rol AS role_id)
        user_result = await db.execute(
            "SELECT id, username, status, role_id, created_at, updated_at FROM users WHERE id = ?",
            [new_id]
        )
        
        if not user_result.rows:
            return None
        
        user_dict = dict(zip(user_result.columns, user_result.rows[0]))
        
        return UserRead(**user_dict)
        
    except Exception as e:
        print("--- ERROR DB FATAL EN USER CONTROLLER ---")
        print(f"Tipo de error: {type(e).__name__}")
        print(f"Mensaje: {e}") 
        print("------------------------------------------")
        raise e 
    finally:
        await db.close()

async def get_users() -> list[UserRead]:
    
    db =Conection()
    
    try:
        result = await db.execute(
            "SELECT * FROM users"
        )

        user_list =[ UserRead(**dict(zip(result.columns, row)))
            for row in result.rows]
            
        return user_list
    
    except Exception as e:
        return {"message": f"{e}"}
    
async def get_user_by_username(username):
    db = Conection()
    try:
        result = await db.execute(
            "SELECT name from users where name = ? ", # Asegúrate de usar 'name' aquí
            [username]
        )

        if not result.rows:
            return False # Usuario no existe
        
        # Si el usuario existe, devolvemos True (o el nombre)
        return True
        
    except Exception as e:
        print(f"Error en get_user_by_username: {e}")
        return False
    finally:
        await db.close() # Aseguramos el cierre

async def get_user_by_id(user_id: int):
    db = Conection()
    try:
        # 1. Seleccionar usando la estructura de la DB
        user_result = await db.execute(
            "SELECT id, username, status, role_id, created_at, updated_at FROM users WHERE id = ?",
            [user_id]
        )
        
        if not user_result.rows:
            return None
        
        # 2. Mapear a Pydantic (UserRead)
        user_dict = dict(zip(user_result.columns, user_result.rows[0]))
        
        return UserRead(**user_dict)
        
    except Exception as e:
        print(f"Error en get_user_by_id: {e}")
        raise e
    finally:
        await db.close()

async def update_user(user_id: int, username: Optional[str], role_id: Optional[int]) -> UserRead:
    db = Conection()
    try:
        # 1. Obtener datos existentes
        existing_user_result = await db.execute(
            "SELECT username, role_id FROM users WHERE id = ?",
            [user_id]
        )
        if not existing_user_result.rows:
            return None 

        # 2. Determinar nuevos valores (usando los nombres de columna de la DB)
        current_username = existing_user_result.rows[0][0] 
        current_role_id = existing_user_result.rows[0][1] 

        new_username = username if username is not None else current_username
        new_role_id = role_id if role_id is not None else current_role_id

        # 3. Ejecutar UPDATE
        update_sql = "UPDATE users SET username = ?, role_id = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
        await db.execute(
            update_sql,
            [new_username, new_role_id, user_id]
        )

        # 4. Obtener el usuario actualizado (SELECT debe coincidir con la DB)
        user_result = await db.execute(
            "SELECT id, username, role_id, created_at, updated_at FROM users WHERE id = ?",
            [user_id]
        )
        
        user_dict = dict(zip(user_result.columns, user_result.rows[0]))
        
        return UserRead(**user_dict)
        
    except Exception as e:
        # Si esto se dispara, es un error de UNIQUE constraint (username duplicado) o de tipo de dato.
        raise e
    finally:
        await db.close()


async def deactivate_user(user_id: int):
    db = Conection()
    try:
        result = await db.execute(
            "DELETE FROM users WHERE ID = ?",
            [user_id]
        )
        if result.rows_affected == 0:
            return False
    except Exception as e:
        print(f"Error al eliminar el usuario: {e}")
        return False
    finally:
        await db.close()
    return True