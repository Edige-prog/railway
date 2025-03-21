from fastapi import APIRouter, Depends, HTTPException, status, Form
from schemas.users import UserInfo, UserCreate, UserLogin, UserUpdate
from repo.users import UserRepository
from utils.security import hash_password, verify_password, create_jwt_token, decode_jwt_token
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Optional
from database.db import get_db
from sqlalchemy.orm import Session
from utils.security import oauth2_scheme


router = APIRouter()


@router.post("/signup")
def get_signup_form(user_info: UserCreate, db: Session = Depends(get_db)):
    user_info.password = hash_password(user_info.password)
    new_user = UserRepository.create_user(user_info, db)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Successfully signed up.", "user_id": new_user.id}
    )


@router.post("/login")
def post_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = UserRepository.get_user_by_email(form_data.username, db)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not verify_password(form_data.password, user.password_hashed):
        raise HTTPException(
            status_code=401,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_jwt_token(user.id)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = UserRepository.get_user_by_id(user_id, db)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    return user


@router.patch("/me")
def patch_user(
        user_input: UserUpdate,
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    user_id = decode_jwt_token(token)
    if "password" in user_input.model_dump(exclude_unset=True):
        user_input.password = hash_password(user_input.new_password)
    updated_user = UserRepository.update_user(user_id, user_input, db)
    return updated_user