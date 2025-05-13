from fastapi import APIRouter, HTTPException, Query

from database.database import Database
from config import Config

from ..models.models import ChatModel

import uuid


router = APIRouter(
    prefix="/chats",
    tags=["chats"],
    responses={404: {"description": "Not found"}}
)

cfg = Config()
db = Database(
    host=cfg.DB_INFO['host'],
    user=cfg.DB_INFO['user'],
    password=cfg.DB_INFO['password'],
    database=cfg.DB_INFO['database']
)

@router.get("/")
async def root_chats():
    """Get all chats from the database."""
    return ({"message": "Hello from chats!"})

@router.get("/get_all_chats")
async def get_chats(user_id: int = Query(..., description="User ID of the user")):
    """Get all chats from the database."""
    
    try:
        chats = await db.get_all_chats(user_id=user_id)
        if chats:
            return (
                {"data": {
                    "chats": chats,
                    "status": "found"
                },
                "meta": {}}
            )
        else:
            raise HTTPException(404, detail="No chats found")
        
    except ValueError as e:
        raise HTTPException(409, detail=str(e))
    
    except RuntimeError as e:
        raise HTTPException(500, detail="Internal server error")
    
@router.post("/create")
async def create_chat(chat: ChatModel):
    """Create a new chat in the database."""
    
    try:
        chat = await db.add_chat(
            chat_id=uuid.uuid4(),
            user_id=chat.user_id,
            title=chat.chat_title,
            model=chat.model
        )
        if chat:
            return (
                {"data": {
                    "chat": chat,
                    "status": "created"
                },
                "meta": {}}
            )
        else:
            raise HTTPException(404, detail="No chats found")
        
    except ValueError as e:
        raise HTTPException(409, detail=str(e))
    
    except RuntimeError as e:
        raise HTTPException(500, detail="Internal server error")
    
@router.delete("/delete")
async def delete_chat(chat_id: str = Query(..., description="Chat ID of the chat")):
    """Delete a chat from the database."""
    
    try:
        chat = await db.delete_chat(chat_id=chat_id)
        if chat:
            return (
                {"data": {
                    "chat": chat,
                    "status": "deleted"
                },
                "meta": {}}
            )
        else:
            raise HTTPException(404, detail="No chats found")
        
    except ValueError as e:
        raise HTTPException(409, detail=str(e))
    
    except RuntimeError as e:
        print(e)
        raise HTTPException(500, detail="Internal server error")
    
