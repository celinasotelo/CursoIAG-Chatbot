from pydantic import BaseModel #para crear modelos de datos

class ChatRequest(BaseModel):
    chat_id: str
    message: str

class ChatResponse(BaseModel):
    chat_id: str
    response: str

class Furniture(BaseModel):
    name: str
    price: int
    description: str

