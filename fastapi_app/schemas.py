from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class Login(BaseModel):
    username: str
    password: str

class Transfer(BaseModel):
    receiver: str
    amount: float
    otp: Optional[str] = None