from fastapi import FastAPI
from app import auth, wallet, admin
from app.scheduler import scheduler
from app.database import init_db

app = FastAPI(title="Wallet")

app.include_router(auth.router, prefix="/auth")
app.include_router(wallet.router, prefix="/wallet")
app.include_router(admin.router, prefix="/admin")

@app.on_event("startup")
def up():
    init_db()
    scheduler.start()
