#package for making unique ids
from uuid import uuid4
from enum import Enum as EnumClass

from sqlalchemy import func, Column, String, Float, DateTime, Integer, Enum, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .db import Base

class Category(str, EnumClass):
    insurance = "Insurance"
    house = "House"
    food = "Food"
    car = "Car"

class Gender(str, EnumClass):
    male = "male"
    female = "female"
    diverse = "diverse"

class DBTransaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    amount = Column(Float)
    receiver = Column(String)
    date = Column(DateTime(timezone=True))
    category = Column(Enum(Category), nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

class DBUser(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True,  autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    email_verified = Column(Boolean, default=False)
    hashed_password = Column(String)
    gender = Column(Enum(Gender), nullable=True)
    age = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())
    transactions = relationship("DBTransaction", primaryjoin="DBUser.id == DBTransaction.user_id", cascade="all, delete-orphan")


