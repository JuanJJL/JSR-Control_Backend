from fastapi import HTTPException, FastAPI, APIRouter
from ..database.User_schema import UserCreate, UserRead, UserUpdate
from ..controllers import UserController


router_users = APIRouter(prefix="/users", tags=["users"])


@router_users.post("/create", response_model=UserRead)
async def create_user_route(data: UserCreate):
    
    if not data.username or len(data.username) < 3:
        raise HTTPException(status_code=400, detail="El nombre de usuario debe tener por lo menos 3 caracteres")
    
    if not data.password or len(data.password) < 8:
        raise HTTPException(status_code=400, detail="La contraseña debe tener por lo menos 8 caracteres")
    
    if data.role_id <= 0:
        raise HTTPException(status_code=400, detail="El rol no puede ser menor o igual a 0")
     
    repeated_user = await UserController.get_user_by_username(data.username)
    if repeated_user:
        raise HTTPException(status_code=409, detail="El usuario ingresado ya está en el sistema")

    try: 
        #El controlador debe devolver el objeto UserRead completo
        new_user = await UserController.create_user(data.username, data.password, data.role_id)
        
        if new_user is None:
             raise Exception("Fallo en el controlador al devolver el usuario.")
             
        return new_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error del servidor: {str(e)}")
    
@router_users.get("/", response_model=list[UserRead]) 
async def get_all_users():
    try:
        users = await UserController.get_users()
        # El controlador debe devolver list[UserRead], si devuelve un dict de error, fallará
        return users 
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router_users.get("/{user_id}", response_model=UserRead) 
async def get_user(user_id: int):
    try:
        user = await UserController.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router_users.put("/update/{user_id}", response_model=UserRead) 
async def update_user(user_id: int, data: UserUpdate):
    try:
        updated_user = await UserController.update_user(user_id, data.username, data.role_id)
        if not updated_user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado o no actualizado")
        return updated_user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router_users.delete("/delete/{user_id}")
async def delete_user(user_id: int):
    try: 
        success = await UserController.deactivate_user(user_id)
        if not success:
            raise HTTPException(status_code=404, detail="Usuario no encontrado para eliminar")
        return {"message": f"Usuario con ID {user_id} eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))