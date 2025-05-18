from fastapi import APIRouter
from app.models import transactions, wallets

router = APIRouter()

@router.get("/flags")
def flags():
    return list(transactions.find({"flagged": True}))

@router.get("/summary")
def summary():
    res = {"INR": 0, "USD": 0}
    for w in wallets.find():
        for c in res:
            res[c] += w["balances"].get(c, 0)
    return res

@router.get("/top-users")
def top():
    data = list(wallets.find())
    data.sort(key=lambda x: sum(x["balances"].values()), reverse=True)
    return data[:5]
