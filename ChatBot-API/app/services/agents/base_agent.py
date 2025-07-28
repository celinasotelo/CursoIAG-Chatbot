from abc import ABC, abstractmethod

class BaseAgent(ABC):
    layer = 'default'

    @abstractmethod
    def generateResponse(self, input_text: str, layer:str) -> str:
        pass

    def uploadDatabase(self) -> str:
        pass

    def searchBySimilarity(self, query: str) -> str:
        pass