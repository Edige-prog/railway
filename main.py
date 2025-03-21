from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from api.auth import router as auth_router
from api.flowers import router as flowers_router
from api.cart import router as cart_router
from database.db import init_tables
import uvicorn

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    init_tables()

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(flowers_router, prefix="/flowers", tags=["flowers"])
app.include_router(cart_router, prefix="/cart", tags=["cart"])
