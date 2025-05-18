from datetime import datetime, timedelta
from app.models import transactions

def fraud_check(uid, amt):
    now = datetime.utcnow()
    before = now - timedelta(minutes=1)
    tx = transactions.find({"user_id": uid, "timestamp": {"$gte": before}})
    if tx.count() >= 3 or amt >= 50000:
        return True
    return False

def scan_all():
    cutoff = datetime.utcnow() - timedelta(days=1)
    txs = transactions.find({
        "timestamp": {"$gte": cutoff},
        "$or": [
            {"amount": {"$gte": 50000}},
            {"type": "transfer"}
        ]
    })

    count = 0
    for t in txs:
        if not t.get("flagged", False):
            transactions.update_one({"_id": t["_id"]}, {"$set": {"flagged": True}})
            count += 1

    print(f"flagged {count}")
