from fastapi import APIRouter, HTTPException, Query

from ..models.models import MessageModel
from database.database import Database
from config import Config

import uuid


router = APIRouter(
    prefix="/messages",
    tags=["messages"],
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
async def root_messages():
    """Get all messages from the database."""
    return ({"message": "Hello from messages!"})

@router.get("/get_all_messages")
async def get_all_messages(chat_id: str = Query(..., title="Chat ID", description="ID of the chat to get messages from")):
    """Get all messages from a chat."""

    try:
        messages = await db.get_all_messages(chat_id=chat_id)
        if messages:
            return (
                {"data": {
                    "messages": messages,
                    "status": "found"
                },
                "meta": {}}
            )
        else:
            raise HTTPException(404, detail="No messages found")
        
    except ValueError as e:
        raise HTTPException(409, detail=str(e))

    except RuntimeError as e:
        raise HTTPException(500, detail="Internal server error")
    
@router.post("/add")
async def message_add(message: MessageModel):
    """Add a new message to a chat."""

    chat_id=str(message.chat_id)
    role=message.role
    content=message.content

    try:
        result = await db.add_message(
            message_id=str(uuid.uuid4()),
            chat_id=chat_id,
            role=role,
            content=content
        )

        if result:
            return (
                {"data": {
                    "chat_id": chat_id,
                    "role": role,
                    "content": content,
                    "status": "created"
                },
                "meta": {}}
            )
        else:
            raise HTTPException(409, detail="Message already exists")
        
    except ValueError as e:
        raise HTTPException(409, detail=str(e))

    except RuntimeError as e:
        raise HTTPException(500, detail="Internal server error")
    
@router.put("/edit")
async def message_edit(message: MessageModel, 
                       message_id: uuid.UUID = Query(..., title="Message ID", description="ID of the message to edit")):
    """Edit a message in a chat."""
    chat_id=str(message.chat_id)
    content=message.content

    try:
        result = await db.edit_message(
            chat_id=chat_id,
            message_id=str(message_id),
            content=content
        )
        if result:
            return (
                {"data": {
                    "chat_id": chat_id,
                    "message_id": message_id,
                    "content": content,
                    "status": "edited"
                },
                "meta": {}}
            )
        else:
            raise HTTPException(409, detail="Message not found")
        
    except ValueError as e:
        raise HTTPException(409, detail=str(e))
    
    except RuntimeError as e:
        raise HTTPException(500, detail="Internal server error")
