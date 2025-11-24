from fastapi import FastAPI
from src.routes.UserRoutes import router_users
from src.routes.AuthRoutes import router



app = FastAPI()

app.include_router(router_users, prefix="/users", tags=["users"])
app.include_router(router, prefix="/auth", tags=["auth"])