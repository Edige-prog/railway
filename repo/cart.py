from fileinput import close
from typing import List

from fastapi import HTTPException, Request
from repo.flowers import FlowersRepository
from schemas.cart import PurchaseItemInfo
from sqlalchemy.orm import Session
from database.models import Purchase, PurchaseItem
from fastapi import Depends
from sqlalchemy import select

from schemas.flowers import FlowerInfo


class CartRepository:
    @classmethod
    def add_purchase(cls, uid: int, db: Session) -> int:
        try:
            new_purchase = Purchase(user_id=uid)
            db.add(new_purchase)
            db.commit()
            db.refresh(new_purchase)  # Load the auto-generated 'id'
            return new_purchase.id
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Failed to create purchase: {str(e)}")


    @classmethod
    def add_purchase_item(cls, pid, fid, quantity, db: Session) -> int:
        try:
            new_purchase_item = PurchaseItem(purchase_id=pid, flower_id=fid, quantity=quantity)
            db.add(new_purchase_item)
            db.commit()
            db.refresh(new_purchase_item)  # Load the auto-generated 'id'
            return new_purchase_item.id
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Failed to create purchase_item: {str(e)}")


    @classmethod
    def get_purchases(cls, uid, db: Session) -> List:
        purchases = db.query(Purchase).filter(Purchase.user_id == uid).all()

        if not purchases:  # Check if the list is empty
            raise HTTPException(status_code=404, detail="Purchases not found")

        result = []
        for purchase in purchases:
            purchase_items = purchase.items
            items = []
            for purchase_item in purchase_items:
                flower = FlowersRepository.get_flower_by_id(purchase_item.flower_id, db)
                items.append(PurchaseItemInfo(id=purchase_item.id, flower = flower, quantity=purchase_item.quantity))
            result.append({"purchase_id": purchase.id, "purchase_items": items})

        return result


    @classmethod
    def get_cart(cls, request:Request, db: Session) -> List:
        val = request.cookies.get("cart")
        if not val:
            return None

        flowers = []
        rows = val.split(';')
        for row in rows:
            if row != '':
                items = row.split(',')
                flower = FlowersRepository.get_flower_by_id(items[0], db)
                quantity = int(items[1])
                flowers.append({'flower':flower, 'quantity':quantity})

        return flowers
