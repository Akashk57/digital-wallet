from app.database import db
from bson.objectid import ObjectId

users = db.users
wallets = db.wallets
transactions = db.transactions

def get_user_by_email(email):
    return users.find_one({"email": email, "deleted": {"$ne": True}})

def create_wallet(user_id):
    wallets.insert_one({
        "user_id": user_id,
        "balances": {"INR": 0, "USD": 0}
    })

def get_wallet(user_id):
    return wallets.find_one({"user_id": user_id})
