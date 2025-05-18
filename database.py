from pymongo import MongoClient
import os

url = os.getenv("MONGO_URL", "mongodb://localhost:27017/")
client = MongoClient(url)
db = client["wallet_system"]

def init_db():
    print("MongoDB connected")
