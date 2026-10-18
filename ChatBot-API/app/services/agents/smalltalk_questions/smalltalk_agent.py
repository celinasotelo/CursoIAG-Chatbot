from chromadb import PersistentClient
from langchain.schema import Document
from langchain_text_splitters import CharacterTextSplitter
from app.services.agents.base_agent import BaseAgent
from app.services.langchain_service import LanchainService
from typing import List, Union
import json 

class SmallTalkAgent(BaseAgent):
    layer = 'smalltalk_questions'
    collection_name = 'smalltalk-collection'

    def __init__(self):
        self.chroma_client = PersistentClient(path="./chroma_db_agents")
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
            for i, chunk in enumerate(chunks):
                documents.append(
                    Document(
                        page_content=f"{item['productName']}\n{chunk}",
                        metadata={"id": f"{item['id']}-{i}"}
                    )
                )

        # upsert con ids fijos: recargar los datos reemplaza en vez de duplicar
        self.collection.upsert(
            ids=[doc.metadata['id'] for doc in documents],
            documents=[doc.page_content for doc in documents],
            metadatas=[doc.metadata for doc in documents]
        )
        return "Base vectorial actualizada."

    def searchBySimilarity(self, query: str):
        results = self.collection.query(query_texts=[query], n_results=3)
        return results
