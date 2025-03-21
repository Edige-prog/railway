from urllib import request

from fastapi import APIRouter, Depends, HTTPException, Request, Form

from ..repo.cart import CartRepository
from ..repo.flowers import FlowersRepository
from ..schemas.flowers import FlowerCreate, FlowerInfo
import uuid
from fastapi.responses import RedirectResponse, JSONResponse
from ..utils.security import decode_jwt_token, oauth2_scheme
from ..database.db import get_db
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/")
def get_cart_items(request: Request, db: Session = Depends(get_db)):
    cart = CartRepository.get_cart(request, db)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart is empty")
    return cart
    # return templates.TemplateResponse("cart/list.html", {"request": request, "flower": flower, "total": total})


@router.post("/")
def post_cart_items(request: Request, flower_id: int = Form(...), db: Session = Depends(get_db)):
    flower = FlowersRepository.get_flower_by_id(flower_id, db)

    cart = CartRepository.get_cart(request, db)
    cookie_val = ""
    new = True
    if cart:
        for row in cart:
            if row['flower'].id == flower_id:
                cookie_val += f'{row["flower"].id},{row["quantity"] + 1};'
                new = False
            else:
                cookie_val += f'{row["flower"].id},{row["quantity"]};'

    if new:
        cookie_val += f'{flower_id},1'

    r = RedirectResponse(url="/cart", status_code=303)
    r.set_cookie(key="cart", value=cookie_val, httponly=True)
    return r


@router.delete("/")
def delete_cart_item(request: Request, flower_id: int = Form(...), db: Session = Depends(get_db)):
    flower = FlowersRepository.get_flower_by_id(flower_id, db)

    cart = CartRepository.get_cart(request, db)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart is empty")

    cookie_val = ""
    new = True

    for row in cart:
        if row['flower'].id == flower_id:
            if row['quantity'] > 1:
                cookie_val += f'{row["flower"].id},{row["quantity"] - 1};'
            new = False
        else:
            cookie_val += f'{row["flower"].id},{row["quantity"]};'

    if new:
        raise HTTPException(status_code=404, detail="Your cart does not contain this flower")

    r = RedirectResponse(url="/cart", status_code=303)
    r.set_cookie(key="cart", value=cookie_val, httponly=True)
    return r


@router.get("/purchase")
def get_purchase(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db),
):
    uid = decode_jwt_token(token)
    return CartRepository.get_purchases(uid, db)


@router.post("/purchase")
def post_purchase(
        request: Request,
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db),
):
    cart = CartRepository.get_cart(request, db)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart is empty")

    # Check quantities before making any changes
    for row in cart:
        if row['flower'].quantity < row['quantity']:
            raise HTTPException(
                status_code=400,
                detail=f"You're trying to buy {row['quantity']} of {row['flower'].name} flowers. But only {row['flower'].quantity} available."
            )

    user_id = decode_jwt_token(token)

    # Create purchase
    new_purchase_id = CartRepository.add_purchase(user_id, db)

    # Add items and update flower quantities
    for row in cart:
        CartRepository.add_purchase_item(new_purchase_id, row['flower'].id, row['quantity'], db)
        FlowersRepository.buy(row['flower'].id, row['quantity'], db)

    # Clear the cart by setting an expired cookie
    response = JSONResponse(content={"message": "Purchase successful", "purchase_id": new_purchase_id})
    response.delete_cookie(key="cart")
    return response

