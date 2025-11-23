from fastapi import FastAPI
from src.routes.UserRoutes import router_users
from src.routes.AuthRoutes import router_auth
from src.routes.ProductRoutes import router_products

app = FastAPI(
    title="JSR Control Backend",
    description="API para el sistema de control de proyectos",
    version="1.0.0"
)

app.include_router(router=router_auth, prefix="")
app.include_router(router=router_users, prefix="")
app.include_router(router=router_products, prefix="")