from fastapi import APIRouter, HTTPException
from ..database.Auth_schema import Token_response, Login_request
from ..controllers.AuthController import check_credentials, create_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
async def login(credentials: Login_request):
    user = await check_credentials(
        credentials.username,
        credentials.password
    )

    print("hola")

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Usuario o contraseña incorrectos"
        )
    
    print("hola2")

    
    token = create_token(user)

    print("hola3")

    return{
        
        "access_token": token,
        "token_type": "bearer"
    }


