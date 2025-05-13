from fastapi import APIRouter
from storage.storage import ColdStorage
from config import Config

from ..models.models import ChatModelMigration, MessageModelMigration

router = APIRouter(
    prefix="/migrate",
    tags=["migratie"],
    responses={404: {"description": "Not found"}}
)

cfg = Config()
storage = ColdStorage(
    host = cfg.COLD_STORAGE["host"],
    user = cfg.COLD_STORAGE["user"],
    password = cfg.COLD_STORAGE["password"],
    database = cfg.COLD_STORAGE["database"]
)

@router.get("/")
async def root_migrations():
    """Check connection to migrations"""
    return ({"message": "Hello from migrations!"})


@router.post("/migrate_chats")
async def migrate_chats(chat_model: ChatModelMigration):
    result = await storage.migrate_chats(
        chat_id = chat_model.chat_id
    )

    if result:
        return (
            {"data": {
                "status": "complited"
            },
            "meta": {}}
        )
    else:
        return (
            {"data": {
                "status": "no-no-no"
            },
            "meta": {}}
        )
    
@router.post("/migrate_messages")
async def migrate_messages(message_model: MessageModelMigration):
    messages_data = {
        "message_id": message_model.message_id,
        "chat_id": message_model.chat_id,
        "role_compressed": message_model.role,
        "content_compressed": message_model.content,
        "created_at": message_model.created_at
    }
    
    result = await storage.migrate_messages(
        messages_data = messages_data
    )
    
    if result:
        return (
            {"data": {
                "status": "completed"
            },
            "meta": {}}
        )
    else:
        return (
            {"data": {
                "status": "no-no-no"
            },
            "meta": {}}
        )