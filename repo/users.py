from sqlalchemy.orm import Session
from schemas.users import UserCreate, UserInfo, UserUpdate
from pydantic import EmailStr
from fastapi import HTTPException
from database.models import User


class UserRepository:
    @classmethod
    def get_user_by_email(cls, email: EmailStr, db: Session):
        user = db.query(User).filter(User.email == email).first()
        if user:
            return UserInfo(
                id=user.id,
                email=user.email,
                fullname=user.full_name,
                password_hashed=user.password_hash,
                photo_url=user.photo_url
            )
        return None

    @classmethod
    def get_user_by_id(cls, user_id: int, db: Session):
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            return UserInfo(
                id=user.id,
                email=user.email,
                fullname=user.full_name,
                password_hashed=user.password_hash,
                photo_url=user.photo_url
            )
        return None

    @classmethod
    def create_user(cls, user_input: UserCreate, db: Session):
        existing_user = cls.get_user_by_email(user_input.email, db)
        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="User with this email already exists"
            )

        new_user = User(
            email=user_input.email,
            full_name=user_input.fullname,
            password_hash=user_input.password,
            photo_url=user_input.photo_url
        )
        
        try:
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return cls.get_user_by_email(user_input.email, db)
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Failed to create user: {str(e)}"
            )

    @classmethod
    def update_user(cls, user_id: int, user_input: UserUpdate, db: Session):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=404,
                detail="User does not exist"
            )

        update_data = user_input.dict(exclude_unset=True)
        if "fullname" in update_data:
            update_data["full_name"] = update_data.pop("fullname")
        if "password" in update_data:
            update_data["password_hash"] = update_data.pop("password")

        try:
            for key, value in update_data.items():
                setattr(user, key, value)
            db.commit()
            db.refresh(user)
            return cls.get_user_by_id(user_id, db)
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Failed to update user: {str(e)}"
            )