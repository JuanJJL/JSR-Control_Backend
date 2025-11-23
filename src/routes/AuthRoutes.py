from fastapi import APIRouter, HTTPException
from ..database.Auth_schema import Token_response, Login_request
from ..controllers.AuthController import check_credentials, create_token
from ..database.User_schema import UserRead # Necesario para tipar al usuario devuelto

router_auth = APIRouter(tags=["auth"]) # Añadimos tags

@router_auth.post("/login", response_model=Token_response) # Añadimos response_model
async def login(credentials: Login_request):
    
    #verificar credenciales en la base de datos
    user_data = await check_credentials(
        credentials.username,
        credentials.password
    )
    
    if user_data is None:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    #convertir user_data (dict) a modelo User
    user = UserRead(**user_data) 
    
    #generar el token JWT
    token = create_token(user)
    
    #retornar el token en la respuesta
    return Token_response(
        access_token=token,
        token_type="bearer",
        role_id=user.role_id
    )