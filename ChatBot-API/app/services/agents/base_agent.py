from abc import ABC, abstractmethod
from langchain.memory import ConversationBufferMemory

class BaseAgent(ABC):
    layer = 'default'

    @abstractmethod
    def generateResponse(self, input_text: str, chat_id: str) -> str:
        pass

    def uploadDatabase(self) -> str:
        pass

    def searchBySimilarity(self, query: str) -> str:
        pass

    def getMemory(self, chat_id: str) -> ConversationBufferMemory:
        # Una memoria por chat_id, para que cada usuario tenga su propio historial
        if not hasattr(self, 'memories'):
            self.memories = {}
        if chat_id not in self.memories:
            self.memories[chat_id] = ConversationBufferMemory(return_messages=True)
        return self.memories[chat_id]
