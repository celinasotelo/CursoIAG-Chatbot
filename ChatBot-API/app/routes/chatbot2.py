from fastapi import APIRouter, HTTPException
from app.models.mChatbot import ChatRequest, ChatResponse
from app.services.sChatbot2 import ChatbotService2

router = APIRouter()

Chatbot_Service2 = ChatbotService2()

@router.post("/chatt", response_model=ChatResponse)
async def chat(request: ChatRequest):
    print('chat2')
    try:
        return await Chatbot_Service2.get_response(request)
    except Exception as e:
        print("Error en /chatt:", e)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload-data")
def upload_data(layer: str):
    print('upload-data')
    try:
        return Chatbot_Service2.uploadDatabase(layer)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print("Error en /upload-data:", e)
        raise HTTPException(status_code=500, detail=str(e))
