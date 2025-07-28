from fastapi import APIRouter, HTTPException
from app.models.mChatbot import ChatRequest, ChatResponse
from app.services.sChatbot2 import ChatbotService2

router = APIRouter()

Chatbot_Service2 = ChatbotService2()

@router.post("/chatt")
async def chat(request: ChatRequest):
    
    print('chat2')
    response = await Chatbot_Service2.get_response(request)
    return response

@router.post("/upload-data")
def chat(layer: str):
    print('upload-data')
    response = Chatbot_Service2.uploadDatabase(layer)
    return response