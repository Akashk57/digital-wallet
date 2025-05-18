from fastapi import APIRouter, Depends, HTTPException
from app.schemas import Dep, Tran
from app.utils import get_user, log_tx, fraud
from app.models import wallets, users, transactions

router = APIRouter()

@router.post("/deposit")
def dep(data: Dep, u=Depends(get_user)):
    w = wallets.find_one({"user_id": u["_id"]})
    if not w:
        raise HTTPException(404, "no wallet")
    wallets.update_one(
        {"user_id": u["_id"]},
        {"$inc": {f"balances.{data.currency}": data.amount}}
    )
    log_tx(u["_id"], "deposit", data.amount, data.currency)
    return {"msg": "ok"}

@router.post("/withdraw")
def wd(data: Dep, u=Depends(get_user)):
    w = wallets.find_one({"user_id": u["_id"]})
    if w["balances"][data.currency] < data.amount:
        raise HTTPException(400, "no money")
    f = fraud(u["_id"], data.amount)
    wallets.update_one(
        {"user_id": u["_id"]},
        {"$inc": {f"balances.{data.currency}": -data.amount}}
    )
    log_tx(u["_id"], "withdraw", data.amount, data.currency, f)
    return {"msg": "done", "flagged": f}

@router.post("/transfer")
def tf(data: Tran, u=Depends(get_user)):
    to = users.find_one({"email": data.to_email})
    if not to or to["_id"] == u["_id"]:
        raise HTTPException(400, "bad user")
    w = wallets.find_one({"user_id": u["_id"]})
    if w["balances"][data.currency] < data.amount:
        raise HTTPException(400, "no money")
    f = fraud(u["_id"], data.amount)

    wallets.update_one({"user_id": u["_id"]}, {"$inc": {f"balances.{data.currency}": -data.amount}})
    wallets.update_one({"user_id": to["_id"]}, {"$inc": {f"balances.{data.currency}": data.amount}})
    log_tx(u["_id"], "transfer", data.amount, data.currency, f, str(to["_id"]))
    return {"msg": "sent", "flagged": f}

@router.get("/history")
def hist(u=Depends(get_user)):
    return list(transactions.find({"user_id": u["_id"], "deleted": {"$ne": True}}))
