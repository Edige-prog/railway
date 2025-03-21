from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    full_name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    photo_url = Column(String, nullable=True)

    purchases = relationship('Purchase', back_populates='user', cascade="all, delete")


class Flower(Base):
    __tablename__ = 'flowers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    quantity = Column(Integer)
    price = Column(Numeric)

    purchase_items = relationship('PurchaseItem', back_populates='flower', cascade="all, delete")


class Purchase(Base):
    __tablename__ = 'purchase'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    user = relationship('User', back_populates='purchases')
    items = relationship('PurchaseItem', back_populates='purchase', cascade="all, delete")


class PurchaseItem(Base):
    __tablename__ = 'purchase_item'

    id = Column(Integer, primary_key=True, autoincrement=True)
    purchase_id = Column(Integer, ForeignKey('purchase.id', ondelete='CASCADE'), nullable=False)
    flower_id = Column(Integer, ForeignKey('flowers.id', ondelete='CASCADE'), nullable=False)
    quantity = Column(Integer)

    purchase = relationship('Purchase', back_populates='items')
    flower = relationship('Flower', back_populates='purchase_items')