from fastapi import APIRouter, HTTPException
from app.schemas import Reg, Log
from app.models import users, get_user_by_email, create_wallet
from jose import jwt
from passlib.hash import bcrypt
from datetime import datetime, timedelta
import os

router = APIRouter()
JWT_SECRET = os.getenv("JWT_SECRET", "supersecret")

@router.post("/register")
def reg(user: Reg):
    if get_user_by_email(user.email):
        raise HTTPException(400, "exists")
    hashed = bcrypt.hash(user.password)
    res = users.insert_one({
        "username": user.username,
        "email": user.email,
        "password": hashed,
        "deleted": False
    })
    create_wallet(str(res.inserted_id))
    return {"msg": "ok"}

@router.post("/login")
def log(user: Log):
    u = get_user_by_email(user.email)
    if not u or not bcrypt.verify(user.password, u["password"]):
        raise HTTPException(401, "bad creds")
    token = jwt.encode(
        {"user_id": str(u["_id"]), "exp": datetime.utcnow() + timedelta(hours=3)},
        JWT_SECRET
    )
    return {"token": token}
