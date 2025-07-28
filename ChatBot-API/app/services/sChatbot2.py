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
            response = await self.agents_dict.get(layer,None).generateResponse(request.message)
        return ChatResponse(chat_id=request.chat_id, response=response)
        
    
    def uploadDatabase(self, layer:str) -> str:
        if(layer == "furniture-questions"):
            file_path = "./app/services/data/furniture_data.json"
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
        if(layer == "frequent-questions"):
            file_path = "./app/services/data/store-information.txt"
            with open(file_path, "r", encoding="utf-8") as file:
                data = file.read()
        if(layer == "smalltalk-questions"):
            file_path = "./app/services/data/smalltalk.json"
            with open(file_path, "r", encoding="utf-8") as file:
                data = file.read()
        if(layer == "question-evaluator"):
            file_path = "./app/services/data/question_evaluator_data.json"
            with open(file_path, "r", encoding="utf-8") as file:
                data = file.read()

        return self.agents_dict.get(layer,None).uploadDatabase(data)
    

        

