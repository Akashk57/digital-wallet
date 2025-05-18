from apscheduler.schedulers.background import BackgroundScheduler
from app.models import transactions
from datetime import datetime, timedelta

def scan():
    c = datetime.utcnow() - timedelta(days=1)
    f = transactions.find({
        "timestamp": {"$gte": c},
        "$or": [
            {"amount": {"$gte": 50000}},
            {"type": "transfer"}
        ]
    })
    print("scan:", f.count())

scheduler = BackgroundScheduler()
scheduler.add_job(scan, "interval", hours=24)
