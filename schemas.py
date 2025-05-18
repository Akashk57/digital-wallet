from pydantic import BaseModel, EmailStr

class Reg(BaseModel):
    username: str
    email: EmailStr
    password: str

class Log(BaseModel):
    email: EmailStr
    password: str

class Dep(BaseModel):
    currency: str
    amount: float

class Tran(BaseModel):
    currency: str
    amount: float
    to_email: EmailStr
