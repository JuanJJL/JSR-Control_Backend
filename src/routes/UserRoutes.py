from fastapi import APIRouter, Depends, HTTPException, FastAPI
from ..database.User_schema import User , UserUpdate
# o si UserController es un módulo
from ..controllers import UserController


# app = APIRouter(prefix="/users", tags=["users"])
app = FastAPI()


@app.post("/user/create", response_model=User)
async def create_user(
    username: str,
    password: str,
    role_id: int,
):
    try: 
        return await UserController.create_user(username,password,role_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.get("/user")
async def get_all_users():
    try:
        return await UserController.get_users()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.get("/user/{user_id}")
async def get_user(user_id: int):
    try:
        return await UserController.get_users_by_id(user_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.put("/user/update/{user_id}")
async def update_user(user_id: int, data: UserUpdate):
    try:
        return await UserController.update_user(user_id, data.username, data.role_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/users/delete/{user_id}")
async def delete_user(user_id: int):
    try: 
        return await UserController.delete_user(user_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


