from typing import Optional

from pydantic import BaseModel

#these porperties will all models have
class TransactionBase(BaseModel):
    user_id: int
    amount: float
    receiver: Optional[str] = None
    category: Optional[str]

    class Config:
        orm_mode = True

class Transaction(TransactionBase):
    id: int


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    email_verified: bool = False
    hashed_password: str
    gender: Optional[str]
    age: Optional[int]
    is_active: bool = True

    class Config:
        orm_mode = True

class User(UserBase):
    id: int

