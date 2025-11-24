from fastapi import HTTPException, FastAPI, APIRouter
from ..database.User_schema import User, User_create
from ..controllers import UserController



router_users = APIRouter(prefix="/users", tags=["users"])



@router_users.post("/create" )
async def create_user(data: User_create):
    
    if not data.username or len(data.username) < 3:
        raise HTTPException(status_code=400, detail="El nombre de usuario debe tener por lo menos 3 caracteres")
    
    if not data.password or len(data.password) < 8:
        raise HTTPException(status_code=400, detail="La contraseña debe tener por lo menos 8 caracteres")
    
    if data.role_id <= 0:
        raise HTTPException(status_code=400, detail="El rol no puede menor o igual a 0")
     
    repeated_user = await UserController.get_user_by_username(data.username)
    if repeated_user:
        raise HTTPException(status_code=409, detail="El usuario ingresado ya esta en el sistema")

    try: 
        return await UserController.create_user(data.username,data.password,data.role_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail={str(e)})
    
@router_users.get("/")
async def get_all_users():
    try:
        return await UserController.get_users()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router_users.get("/{user_id}")
async def get_user(user_id: int):
    try:
        return await UserController.get_users_by_id(user_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router_users.put("/update/{user_id}")
async def update_user(user_id: int, data: User):
    try:
        return await UserController.update_user(user_id, data.username, data.role_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router_users.delete("/delete/{user_id}")
async def delete_user(user_id: int):
    try: 
        return await UserController.delete_user(user_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


