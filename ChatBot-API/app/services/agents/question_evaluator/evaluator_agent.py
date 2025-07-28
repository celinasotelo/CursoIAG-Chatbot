from app.services.agents.base_agent import BaseAgent
from app.services.langchain_service import LanchainService
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document
from langchain_text_splitters import CharacterTextSplitter
from typing import List, Union
import os
import json 
from langchain.memory import ConversationBufferMemory

class QuestionEvaluator(BaseAgent):
    layer = 'question_evaluator'
    collection_name = 'question-evaluator-collection'

    def __init__(self):
        self.embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
        self.vectorstore = Chroma(
            collection_name=self.collection_name,
            embedding_function=self.embeddings,
            persist_directory="./chroma_db_evaluator" 
        )
        self.langchain_service = LanchainService()

        self.memory = ConversationBufferMemory(return_messages=True)

    async def generateResponse(self, input_text: str, layer: str = "") -> str:
        context = self.searchBySimilarity(input_text)
        self.memory.chat_memory.add_user_message(input_text)
        respuesta = await self.langchain_service.chat(self, input_text, context, memory=self.memory)
        self.memory.chat_memory.add_ai_message(respuesta)
        return respuesta

    def uploadDatabase(self, new_data: Union[str, List[dict]]) -> str:
        if isinstance(new_data, str):
            new_data = json.loads(new_data)
        return self.uploadDatabaseWithChunks(new_data)

    def uploadDatabaseWithChunks(self, new_data: List[dict]) -> str:
        text_splitter = CharacterTextSplitter(
            separator=" ",
            chunk_size=200,
            chunk_overlap=20
        )
        
        documents = []
        for item in new_data:
            chunks = text_splitter.split_text(item['question'])
            for chunk in chunks:
                documents.append(
                    Document(
                        page_content=f"{chunk}\nCategory: {item['category']}",
                        metadata={"id": str(item["id"])}
                    )
                )
        
        print("Documentos a insertar: " + str(len(documents)))
        
        self.vectorstore.add_documents(documents)
        
        return "Base vectorial actualizada."

    def searchBySimilarity(self, query: str) -> str:
        retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})
        docs = retriever.get_relevant_documents(query)
        concatenated_docs = "\n".join([doc.page_content for doc in docs])
        return concatenated_docs