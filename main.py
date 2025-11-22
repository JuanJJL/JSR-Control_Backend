from fastapi import FastAPI
from src.routes.UserRoutes import router_users


app = FastAPI()

app.include_router(router_users, prefix="/users", tags=["users"])