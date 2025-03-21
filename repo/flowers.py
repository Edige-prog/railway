from xmlrpc.client import ResponseError
from schemas.flowers import FlowerCreate, FlowerInfo
from fastapi import HTTPException
from sqlalchemy.orm import Session
from database.models import Flower
from sqlalchemy import update


class FlowersRepository:
    @classmethod
    def create_flower(cls, flower: FlowerCreate, db: Session):
        try:
            new_flower = Flower(
                name=flower.name,
                quantity=flower.quantity,
                price=flower.price
            )
            db.add(new_flower)
            db.commit()
            db.refresh(new_flower)
            return cls.get_flower_by_id(new_flower.id, db)
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Failed to create flower: {str(e)}"
            )

    @classmethod
    def get_all_flowers(cls, db: Session):
        flowers = db.query(Flower).order_by(Flower.id.desc()).all()
        if not flowers:
            raise HTTPException(status_code=404, detail="No flowers found")
        return [FlowerInfo(
            id=flower.id,
            name=flower.name,
            quantity=flower.quantity,
            price=flower.price
        ) for flower in flowers]

    @classmethod
    def get_flower_by_id(cls, flower_id: int, db: Session):
        flower = db.query(Flower).filter(Flower.id == flower_id).first()
        if not flower:
            raise HTTPException(status_code=404, detail="Flower not found")
        return FlowerInfo(
            id=flower.id,
            name=flower.name,
            quantity=flower.quantity,
            price=flower.price
        )

    @classmethod
    def delete_flower_by_id(cls, flower_id: int, db: Session):
        flower = db.query(Flower).filter(Flower.id == flower_id).first()
        if not flower:
            raise HTTPException(status_code=404, detail="Flower not found")

        try:
            db.delete(flower)
            db.commit()
            return {"message": "Flower deleted successfully"}
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Failed to delete flower: {str(e)}"
            )

    @classmethod
    def buy(cls, flower_id: int, quantity: int, db: Session):
        flower = db.query(Flower).filter(Flower.id == flower_id).first()
        if not flower:
            raise HTTPException(status_code=404, detail="Flower not found")
        
        if flower.quantity < quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Not enough flowers available. Only {flower.quantity} left."
            )

        try:
            flower.quantity -= quantity
            db.commit()
            db.refresh(flower)
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Failed to update flower quantity: {str(e)}"
            )

