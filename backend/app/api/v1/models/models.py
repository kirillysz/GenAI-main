from pydantic import BaseModel

class UserModel(BaseModel):
    telegram_id: int

class ChatModel(BaseModel):
    user_id: int
    chat_title: str
    model: str = "llama3.2"
    
class MessageModel(BaseModel):
    chat_id: str
    role: str = "user"
    content: str


class ChatModelMigration(BaseModel):
    chat_id: str

class MessageModelMigration(MessageModel):
    message_id: str
    created_at: int



class ChatRequest(BaseModel):
    chat_id: str
    messages: list[dict]
    model: str = 'llama3.1'