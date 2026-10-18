import json
import os
from dotenv import load_dotenv, find_dotenv

from app.models.mChatbot import ChatRequest, ChatResponse, Furniture
from app.services.agents.frequent_questions.frequent_agent import FrequentQuestionAgent
from app.services.agents.furniture_questions.furniture_agent import FurnitureAgent
from app.services.agents.question_evaluator.evaluator_agent import QuestionEvaluator
from app.services.agents.assistant_questions.assistant_agent import AssistantQuestionAgent
from app.services.agents.smalltalk_questions.smalltalk_agent import  SmallTalkAgent

import openai
load_dotenv(find_dotenv())

class ChatbotService2:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = self.openai_api_key

        self.agents_dict = {
            "furniture-questions": FurnitureAgent(),
            "frequent-questions": FrequentQuestionAgent(),
            "question-evaluator": QuestionEvaluator(),
            "assistant-questions": AssistantQuestionAgent(),
            "smalltalk-questions": SmallTalkAgent()
        }   

    async def get_response(self, request:ChatRequest) -> str:
        responseQuestionEvaluator = await self.agents_dict.get("question-evaluator",None).generateResponse(request.message, "")
        layer = None
        if(responseQuestionEvaluator == "furniture-questions"):
            layer = "furniture-questions"
        if(responseQuestionEvaluator == "frequent-questions"):
            layer = "frequent-questions"
        if(responseQuestionEvaluator == "assistant-questions"):
            layer = "assistant-questions"
        if(responseQuestionEvaluator == "smalltalk-questions"):
            layer = "smalltalk-questions"

        print('responseQuestionEvaluator: ' + str(responseQuestionEvaluator))
        print('layer: ' + str(layer))
        if layer == None:
            response = 'No tengo información sobre ese tema. Puedo ayudarte en algo más?'
        else:
            response = await self.agents_dict.get(layer,None).generateResponse(request.message, request.chat_id)
        return ChatResponse(chat_id=request.chat_id, response=response)
        
    
    # Archivo de datos de cada capa y si se carga como JSON (lista) o como texto
    DATA_FILES = {
        "furniture-questions": ("./app/services/data/furniture_data.json", True),
        "frequent-questions": ("./app/services/data/store-information.txt", False),
        "smalltalk-questions": ("./app/services/data/smalltalk.json", False),
        "question-evaluator": ("./app/services/data/question_evaluator_data.json", False),
    }

    def uploadDatabase(self, layer:str) -> str:
        if layer not in self.DATA_FILES:
            raise ValueError(f"Capa inválida: '{layer}'. Opciones: {', '.join(self.DATA_FILES)}")

        file_path, is_json = self.DATA_FILES[layer]
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file) if is_json else file.read()

        return self.agents_dict[layer].uploadDatabase(data)
