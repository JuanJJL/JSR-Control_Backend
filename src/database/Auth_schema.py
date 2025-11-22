from pydantic import BaseModel

class Login_request(BaseModel):
    username: str
    password: str

class Token_response(BaseModel):
    access_token: str
    token_type: str
    role_id: int
    



