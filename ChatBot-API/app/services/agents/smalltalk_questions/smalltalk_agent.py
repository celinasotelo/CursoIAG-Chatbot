from chromadb import Client
from chromadb.config import Settings
from langchain.schema import Document
from langchain_text_splitters import CharacterTextSplitter
from app.services.agents.base_agent import BaseAgent
from app.services.langchain_service import LanchainService
import random
from typing import List, Union
import json 

class SmallTalkAgent(BaseAgent):
    layer = 'smalltalk_questions'
    collection_name = 'smalltalk-collection'

    def __init__(self):
        self.chroma_client = Client(Settings(chroma_server_host="localhost", chroma_server_http_port="8000"))
        self.collection = self.chroma_client.get_or_create_collection(name=self.collection_name)
        self.langchain_service = LanchainService()

    async def generateResponse(self, input_text: str, chat_id: str) -> str:
        context = self.searchBySimilarity(input_text)
        concatenated_docs = ""
        for doc_list in context['documents']:
            for doc in doc_list:
                concatenated_docs += doc + "\n"

        respuesta = await self.langchain_service.chat(self, input_text, concatenated_docs, memory=self.getMemory(chat_id))
        return respuesta

    def uploadDatabase(self, new_data: Union[str, List[str]]):
        if isinstance(new_data, str):
            new_data = json.loads(new_data)
        return self.uploadDatabaseWithChunks(new_data)

    def uploadDatabaseWithChunks(self, new_data: List[dict]):
        text_splitter = CharacterTextSplitter(separator=" ", chunk_size=200, chunk_overlap=20)
        documents = []

        for item in new_data:
            chunks = text_splitter.split_text(item['description'])
            for chunk in chunks:
                documents.append(
                    Document(
                        page_content=f"{item['productName']}\n{chunk}",
                        metadata={"id": str(item["id"])}
                    )
                )

        self.collection.add(
            ids=[doc.metadata['id'] + str(random.randint(1, 10000)) for doc in documents],
            documents=[doc.page_content for doc in documents],
            metadatas=[doc.metadata for doc in documents]
        )
        return "Base vectorial actualizada."

    def searchBySimilarity(self, query: str):
        results = self.collection.query(query_texts=[query], n_results=3)
        return results
