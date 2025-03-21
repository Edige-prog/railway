from fastapi import APIRouter, Depends, HTTPException, Request, Form
from repo.flowers import FlowersRepository
from schemas.flowers import FlowerCreate, FlowerInfo
from fastapi.responses import RedirectResponse
from database.db import get_db
from sqlalchemy.orm import Session

router = APIRouter()


# GET /flowers - для показа списка цветов
# POST /flowers - добавление цветов
@router.get("/")
async def get_all_flowers(db: Session = Depends(get_db)):
    flowers = FlowersRepository.get_all_flowers(db)
    return flowers

@router.post("/")
async def create_flower(flower: FlowerCreate, db: Session = Depends(get_db)):
    flower = FlowerCreate(name=flower.name, price=flower.price, quantity=flower.quantity)
    FlowersRepository.create_flower(flower, db)
    return RedirectResponse(url="/flowers", status_code=303)

@router.post("/{flower_id}", response_model=FlowerInfo)
async def get_flower_by_id(flower_id: int, db: Session = Depends(get_db)):
    flower = FlowersRepository.get_flower_by_id(flower_id, db)
    return flower

@router.delete("/{flower_id}")
async def delete_flower(flower_id: int, db: Session = Depends(get_db)):
    message = FlowersRepository.delete_flower_by_id(flower_id, db)
    return message