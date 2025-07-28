from chromadb import Client
from app.services.agents.base_agent import BaseAgent
from chromadb.config import Settings
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from typing import List, Union
from app.services.langchain_service import LanchainService 
import os
from langchain.memory import ConversationBufferMemory

class FrequentQuestionAgent(BaseAgent):
    layer = 'frequent_questions'
    collection_name = 'frequent-question-collection'

    def __init__(self):
        self.chroma_client = Client(Settings(chroma_server_host="localhost", chroma_server_http_port="8000"))
        self.collection = self.chroma_client.get_or_create_collection(name=self.collection_name)
        self.langchain_service = LanchainService()
        self.memory = ConversationBufferMemory(return_messages=True)

    async def generateResponse(self, input_text: str) -> str:
        context = self.searchBySimilarity(input_text)
        concatenated_docs = ""
        for doc_list in context['documents']:
            for doc in doc_list:
                concatenated_docs += doc + "\n"   

        respuesta = await self.langchain_service.chat(self, input_text, concatenated_docs, memory=self.memory)
        return respuesta
        
    def uploadDatabase(self, new_data: Union[str, List[str]]):
        return self.uploadDatabaseWithoutChunks(new_data)
    
    def uploadDatabaseWithoutChunks(self, new_data: Union[str, List[dict]]):
        documents = [
            Document(
                page_content=new_data,
                metadata={"id": "1"}  
            )
        ]

        print("frecuent information:" + str(documents[0].page_content))

        self.collection.add(
            ids=["1"],
            documents=documents[0].page_content,
            metadatas=documents[0].metadata
        )
        
        return "Base vectorial actualizada."

    def searchBySimilarity(self, query: str) -> str:
        results = self.collection.query(
            query_texts=[query], 
            n_results=3  
        )
        return results
