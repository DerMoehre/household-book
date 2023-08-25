from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated

from sqlalchemy.orm import Session

from .models import DBTransaction, DBUser, Category
from .schemas import Transaction, UserBase
from .db import engine
from app.auth import oauth2_scheme

import pandas as pd

#methods for interacting with database

#<---------TRANSACTION--------->

def get_transaction(db: Session, transaction_id: int):
    return db.query(DBTransaction).where(DBTransaction.id == transaction_id).first()

def get_transactions(db: Session):
    return db.query(DBTransaction).all()

def get_transactions_user(db: Session, user_id: int):
    return db.query(DBTransaction).where(DBTransaction.user_id == user_id).all()

def create_transaction_m(db: Session, transaction: Transaction):
    db_transaction = DBTransaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)

    return db_transaction

def create_transaction_i(transaction):
    transaction.to_sql('transactions', engine, if_exists='append', index=False)
    return "Import Successful"

def delete_transaction(db: Session, transaction_id: int):
    target = db.query(DBTransaction).where(DBTransaction.id == transaction_id).first()
    db.delete(target)
    db.commit()

    return "Successful deleted"

def transaction_by_category(db: Session, category: Category):
    return db.query(DBTransaction).where(DBTransaction.category == category and DBTransaction.user_id == 0).all()

#<---------USER--------->

def get_user(db: Session, user_id: int):
    return db.query(DBUser).where(DBUser.id == user_id).first()

def get_users(db: Session):
    return db.query(DBUser).all()

def get_user_by_mail(db:Session, mail, password):
    # the user query should be done with the pydantic model schema
    user = db.query(DBUser).where(DBUser.email == mail and DBUser.hashed_password == password).first()
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect mail or password")
    
    return {"access_token": user.email, "token_type": "bearer"}


def create_user(db: Session, user: UserBase):
    db_user = DBUser(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def fake_decode_token(token):
    return UserBase(
        first_name= token + "Test", last_name="User", email="test@test.com", hashed_password="1234"
    )

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    return user

#<---------OTHERS--------->
def import_data():
    df = pd.read_csv('test.csv', delimiter=';')
    return df



