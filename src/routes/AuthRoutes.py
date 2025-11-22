from fastapi import APIRouter
from ..database.Auth_schema import Token_response, Login_request
from ..controllers.AuthController import check_credentials

router = APIRouter()

@router.post("/login")
async def login(credentials: Login_request):
    user = await check_credentials(
        credentials.username,
        credentials.password
    )
