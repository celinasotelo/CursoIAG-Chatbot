import json
from langchain_text_splitters import CharacterTextSplitter
from app.services.agents.base_agent import BaseAgent
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document
from typing import List, Union
from app.services.langchain_service import LanchainService
import os

class FurnitureAgent(BaseAgent):
    layer = 'furniture_questions'
    collection_name = 'furniture-collection'

    def __init__(self):
        self.embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
        self.vectorstore = Chroma(
            collection_name=self.collection_name,
            embedding_function=self.embeddings,
            persist_directory="./chroma_db"
        )
        self.langchain_service = LanchainService()

    async def generateResponse(self, input_text: str, chat_id: str) -> str:
        context = self.searchBySimilarity(input_text)
        memory = self.getMemory(chat_id)
        memory.chat_memory.add_user_message(input_text)
        respuesta = await self.langchain_service.chat(self, input_text, context, memory=memory)
        memory.chat_memory.add_ai_message(respuesta)
        return respuesta

    def uploadDatabase(self, new_data: Union[str, List[dict]]):
        return self.uploadDatabaseWithChunks(new_data)

    def uploadDatabaseWithChunks(self, new_data: List[dict]):
        text_splitter = CharacterTextSplitter(
            separator=" ",
            chunk_size=500,
            chunk_overlap=50
        )
        
        documents = []
        for product in new_data:
            chunks = text_splitter.split_text(product['description'])
            for i, chunk in enumerate(chunks):
                documents.append(
                    Document(
                        page_content=f"{product['productName']}\n{chunk}\nPrecio: {product['price']}",
                        metadata={"id": f"{product['id']}-{i}"}
                    )
                )

        print("Documentos a insertar: " + str(len(documents)))

        # ids fijos: recargar los datos reemplaza en vez de duplicar
        self.vectorstore.add_documents(documents, ids=[doc.metadata["id"] for doc in documents])
        
        return "Base vectorial actualizada."

    def uploadDatabaseWithoutChunks(self, new_data: List[dict]):
        documents = [
            Document(
                page_content=f"{product['productName']}\n{product['description']}\nPrecio: {product['price']}",
                metadata={"id": str(product["id"])}
            )
            for product in new_data
        ]
        
        print("Documentos a insertar: " + str(len(documents)))
        
        self.vectorstore.add_documents(documents)
        self.vectorstore.persist()
        
        return "Base vectorial actualizada."

    def searchBySimilarity(self, query: str) -> str:
        retriever = self.vectorstore.as_retriever(search_kwargs={"k": 5})
        docs = retriever.get_relevant_documents(query)
        concatenated_docs = "\n".join([doc.page_content for doc in docs])
        return concatenated_docs