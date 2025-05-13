from fastapi import FastAPI
from .routers import users, chats, messages, migarations, chat_neuro

from database.database import Database
from storage.storage import ColdStorage
from config import Config

root = FastAPI(
    title="GENAI API",
    version="1.0.0",
)
cfg = Config()

db = Database(
    host = cfg.DB_INFO["host"],
    user = cfg.DB_INFO["user"],
    password = cfg.DB_INFO["password"],
    database = cfg.DB_INFO["database"]
)
cs = ColdStorage(
    host = cfg.COLD_STORAGE["host"],
    user = cfg.COLD_STORAGE["user"],
    password = cfg.COLD_STORAGE["password"],
    database = cfg.COLD_STORAGE["database"]
)

@root.on_event("startup")
async def on_startup():
    await db.init_db()
    await cs.init_tables()

root.include_router(
    users.router
)

root.include_router(
    chats.router
)

root.include_router(
    messages.router
)


root.include_router(
    migarations.router
)

root.include_router(
    chat_neuro.router
)