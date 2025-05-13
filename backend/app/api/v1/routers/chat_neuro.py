from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from ..models.models import ChatRequest
from neuro.model_stream import Model, UnsupportedModelError
from database.database import Database

from config import Config

import uuid

router = APIRouter(
    prefix="/neuro"
)

cfg = Config()
db = Database(
    host=cfg.DB_INFO["host"],
    user=cfg.DB_INFO["user"],
    password=cfg.DB_INFO["password"],
    database=cfg.DB_INFO["database"]
)

@router.post("/chat")
async def chat_stream(chat_request: ChatRequest):
    try:
        message_id = str(uuid.uuid4())
        previous_messages = await db.get_all_messages(chat_id=chat_request.chat_id) or []

        context_messages = [
            {"role": msg["role"], "content": msg["content"]}
            for msg in previous_messages
        ]

        for message in chat_request.messages:
            await db.add_message(
                message_id=message_id,
                chat_id=chat_request.chat_id,
                role=message["role"],
                content=message["context"]
            )
            context_messages.append({
                "role": message["role"],
                "content": message["context"]
            })

        model = Model(chat_request.model)
        answer = await model.generate_answer(messages=context_messages)
        
        await db.add_message(
            message_id=str(uuid.uuid4()),
            chat_id=chat_request.chat_id,
            role="assistant",
            content=answer
        )

        return JSONResponse(content={"data": answer.strip()})

    except UnsupportedModelError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))