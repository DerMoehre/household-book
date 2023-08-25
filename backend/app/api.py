from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm

from typing import List, Annotated

from app.auth import oauth2_scheme

from app.actions import *
from app.schemas import TransactionBase, Transaction, UserBase, User
from app.db import get_db, engine
import app.models as models
from app.models import Category, DBUser

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.post("/login/", tags=["login"])
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    return get_user_by_mail(db, form_data.username, form_data.password)

#<---------TRANSACTION--------->

@app.post("/transactions/create/", response_model=TransactionBase, tags=["transactions"])
def create_transaction_manual(transaction: TransactionBase, db: Session = Depends(get_db)):
    db_transaction_manual = create_transaction_m(db, transaction)
    return db_transaction_manual

@app.post("/transactions/import/", tags=["transactions"])
def create_transaction_import():
    db_transaction_import = create_transaction_i(import_data())
    return db_transaction_import

@app.get("/transactions/", response_model=List[Transaction], tags=["transactions"])
def get_all_transactions(db: Session = Depends(get_db)):
    return get_transactions(db)

@app.get("/transactions/{transactions_id}", tags=["transactions"])
def get_transaction_by_id(transaction_id: int, db: Session = Depends(get_db)):
    return get_transaction(db, transaction_id)

@app.get("/transactions/delete/{transactions_id}", tags=["transactions"])
def delete_transaction_by_id(transaction_id: int, db: Session = Depends(get_db)):
    return delete_transaction(db, transaction_id)

@app.get("/transactions/{category}/", tags=["transactions"])
def get_transaction_by_category(category: Category, db: Session = Depends(get_db)):
    return transaction_by_category(db, category)

#<---------USER-TRANSACTION--------->

@app.get("/{user_id}/transactions/", tags=["user-transaction"])
def get_user_transactions(user_id: int, db: Session = Depends(get_db)):
    return get_transactions_user(db, user_id)

#<---------USER--------->

@app.post("/users/", response_model=UserBase, tags=["users"])
def create_user_view(transaction: UserBase, db: Session = Depends(get_db)):
    db_transaction = create_user(db, transaction)
    return db_transaction

@app.get("/users/", response_model=List[User], tags=["users"])
def get_users_view(db: Session = Depends(get_db)):
    return get_users(db)

@app.get("/users/{user_id}", response_model=User, tags=["users"])
def get_user_view(user_id: int, db: Session = Depends(get_db)):
    return get_user(db, user_id)

@app.get("/users/me/", tags=["users"])
async def read_users_me(current_user: Annotated[UserBase, Depends(get_current_user)]):
    return current_user

#<---------DATA--------->
@app.get("/data/", tags=["data"])
def load_data():
    return import_data()







