from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from app.services.agents.base_agent import BaseAgent
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.schema.messages import SystemMessage, HumanMessage

class LanchainService():

    async def getInstruction(self,  agent: BaseAgent) -> str:

        with open('./app/services/agents/' + agent.layer + '/instruction.txt', 'r', encoding='utf-8') as file:
            instruction = file.read()

        return instruction


    async def chat(self, agent: BaseAgent, inputMessage: str, context: str, memory: ConversationBufferMemory) -> str:
        try:
            model = ChatOpenAI(
                model="gpt-4o",
                temperature=0.5,
            )

            inputSystem = await self.getInstruction(agent)

            full_system_message = inputSystem.replace("{Context}", context)

            memory.chat_memory.add_message(SystemMessage(content=full_system_message))
            memory.chat_memory.add_message(HumanMessage(content=inputMessage))

            conversation = ConversationChain(
                llm=model,
                memory=memory,
                verbose=False
            )

            response = conversation.predict(input=inputMessage)

            return response
        except Exception as e:
            print("Langchain chat error:", e)
            raise e
