from jose import jwt, JWTError
from fastapi import Header, HTTPException
from app.models import users, transactions
from datetime import datetime
from bson.objectid import ObjectId
import os

key = os.getenv("JWT_SECRET", "supersecret")

def get_user(Authorization: str = Header(...)):
    try:
        token = Authorization.split()[1]
        data = jwt.decode(token, key)
        u = users.find_one({"_id": ObjectId(data["user_id"])})
        if not u:
            raise HTTPException(401, "not found")
        return u
    except JWTError:
        raise HTTPException(401, "bad token")

def log_tx(uid, typ, amt, cur, flag=False, to=None):
    transactions.insert_one({
        "user_id": uid,
        "type": typ,
        "to": to,
        "amount": amt,
        "currency": cur,
        "timestamp": datetime.utcnow(),
        "flagged": flag,
        "deleted": False
    })

def fraud(uid, amt):
    recent = transactions.find({"user_id": uid}).sort("timestamp", -1).limit(3)
    return sum(1 for _ in recent) >= 3 or amt >= 50000
