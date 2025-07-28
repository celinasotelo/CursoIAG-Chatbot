# Chatbot de Venta de Muebles con Clasificación, Persistencia y Memoria
Este proyecto implementa un chatbot de ventas de muebles con FastAPI, que responde preguntas sobre productos, información de tienda y otras consultas. Utiliza LangChain, OpenAI, ChromaDB y una arquitectura basada en agentes para especializar respuestas. El chatbot también cuenta con memoria conversacional, permitiendo mantener el contexto durante la charla.

**Tecnologías Utilizadas**
-FastAPI, para construir la API web.
-LangChain, para la lógica del chatbot y de los agentes.
-OpenAI GPT-4o, para generar las respuestas.
-ChromaDB, para persistencia y búsqueda semántica de documentos.
-ConversationBufferMemory, para mantener contexto en cada sesión.

**Funcionalidad del ChatBot**
El agente 'QuestionEvaluator' clasifica la intención del usuario en cada mensaje que envía, y según esto lo deriva al agente correcto que puede resolver su petición.

Agentes: 
-furniture-questions: Responde preguntas sobre los productos disponibles en la tienda
-frequent-questions: Responde informació general de la tienda
-assistant-questions: Se encarga de derivar al usuario con una persona real cuando este lo requiere, brindandole un número de whatsapp
-smalltalk-questions: Responde educadamente cuando el usuario saluda o agradece.

Una vez detectado el agente correcto, el chatbot:
Utiliza búsqueda semántica con ChromaDB para recuperar contexto relevante.
Genera la respuesta usando el modelo GPT-4o, incluyendo la memoria de conversación para mantener coherencia.
Todas las respuestas son influenciadas por un archivo instruction.txt propio de cada agente.

Si no es posible detectar ningún agente(esto ocurre cuando el usuario realiza una pregunta que no está relacionada con la tienda), se genera una respuesta para informar al usuario que no es posible responder esa pregunta. Esto ocurre en el archivo 'sChatbot2.py' cuando el layer es None --> if layer == None:
            response = 'No tengo información sobre ese tema. Puedo ayudarte en algo más?'
        else: ...


**Uso por API**
   `POST /chat`: Este endpoint acepta un `chat_id` y un `message` como cuerpo de la solicitud y devuelve una respuesta del chatbot.
   Se encuentra en http://127.0.0.1:8002/docs
Ejemplo de solicitud:
{
  "chat_id": "123",
  "message": "cuanto sale la lampara de pie industrial?"
}
Respuesta esperada:
{
  "chat_id": "123",
  "response": "La Lámpara de Pie Industrial cuesta 120 USD."
}

Desde esta interfaz también se cargan los datos de cada agente, información que se encuentra en services/data/, y el chatbot puede responder en base a ello

**Memoria de Conversación**
Cada agente tiene memoria por sesión (ConversationBufferMemory), lo que permite que el bot recuerde lo que el usuario preguntó antes y responda con coherencia.
Ejemplo de interacción con memoria:

You - 03:30 a. m.
cuanto cuesta el sofa minimalista?

Chatbot - 03:30 a. m.
El Sofá Minimalista cuesta 500 USD.

You - 03:31 a. m.
de que esta hecho?

Chatbot - 03:31 a. m.
El Sofá Minimalista está tapizado en tela de alta calidad, lo que le da una apariencia elegante y duradera. Su estructura está hecha de madera maciza, lo que asegura su resistencia y durabilidad. Los cojines están generosamente rellenos para proporcionar una comodidad inigualable.

**Estructura del Proyecto**
├── app/
│   ├── main.py
│   ├── routes/
│   │   └── chatbot.py
|   |   |__ chatbot2.py
│   ├── services/
│   │   ├── sChatbot.py
│   │   ├── sChatbot2.py
│   │   ├── langchain_service.py
│   │   └── data/
│   │   └── agents/
│   │       ├── furniture_questions/
│   │       │   └── furniture_agent.py
│   │       |    └── instruction.txt
│   │       ├── smalltalk_questions/
│   │       │   └── smalltalk_agent.py
│   │       |    └── instruction.txt
│   │       ├── frequent_questions/
│   │       │   └── frequent_agent.py
│   │       |    └── instruction.txt
│   │       ├── question_evaluator/
│   │       │   └── evaluator_agent.py
│   │       |    └── instruction.txt
│   │       └── assistant_questions/
│   │           └── assistant_agent.py
│   │            └── instruction.txt
|   └── models
│        └── mChatbot.py
├── .env
├── requirements.txt
└── README.md

**Ejecución**
1. Iniciar el entorno en Anaconda
2. Instalar dependencias 
    pip install -r requirements.txt
3. Correr el servidor 
    uvicorn app.main:app --reload --host 127.0.0.1 --port 8002
4. El chatbot estará disponible en:
    http://localhost:8000/
