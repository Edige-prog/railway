from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from app.api.auth import router as auth_router
from app.api.flowers import router as flowers_router
from app.api.cart import router as cart_router
import uvicorn

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(flowers_router, prefix="/flowers", tags=["flowers"])
app.include_router(cart_router, prefix="/cart", tags=["cart"])

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)