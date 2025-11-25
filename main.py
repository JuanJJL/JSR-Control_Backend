from fastapi import FastAPI
from src.routes.UserRoutes import router_users
from src.routes.AuthRoutes import router
from src.routes.ClientsRoutes import router_clients



app = FastAPI()

app.include_router(router_users, prefix="/users", tags=["users"])
app.include_router(router, prefix="/auth", tags=["auth"])
app.include_router(router_clients, prefix="/clientes",tags=["clients"])