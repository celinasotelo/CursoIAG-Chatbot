from fastapi import APIRouter, HTTPException
from app.models.mChatbot import ChatRequest, ChatResponse
from app.services.sChatbot import ChatbotService

router = APIRouter()

chatbot_service = ChatbotService()

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        response = chatbot_service.get_response(request.chat_id, request.message)
        return ChatResponse(chat_id=request.chat_id, response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))