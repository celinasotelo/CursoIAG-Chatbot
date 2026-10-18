from chromadb import Client
from app.services.agents.base_agent import BaseAgent
from chromadb.config import Settings
from app.services.langchain_service import LanchainService 

class AssistantQuestionAgent(BaseAgent):
    layer = 'assistant_questions'
    collection_name = 'assistant-question-collection'

    def __init__(self):
        self.chroma_client = Client(Settings(chroma_server_host="localhost", chroma_server_http_port="8000"))
        self.collection = self.chroma_client.get_or_create_collection(
            name=self.collection_name
        )
        self.langchain_service = LanchainService()
        
        self.derivation_keywords = ["humano", "asesor", "persona", "ayuda real", "problema distinto"]

    async def generateResponse(self, question: str, chat_id: str) -> str:
        lower_question = question.lower()
        
        if any(palabra in lower_question for palabra in self.derivation_keywords):
            return (
                "Puedo derivarte con un asesor humano. "
                "Escríbele directamente por WhatsApp --> "
                "https://wa.me/5493795066238"
            )
        try:
            response = await self.langchain_service.chat(self, question, "", memory=self.getMemory(chat_id))
            return response
        except Exception:
            return "Estoy teniendo problemas para responder eso ahora mismo. ¿Querés que te derive con un asesor humano?"

