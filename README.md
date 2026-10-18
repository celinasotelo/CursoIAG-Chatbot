# Chatbot de Venta de Muebles con Agentes, RAG y Memoria

Chatbot de atención al cliente para la mueblería **Muebles "El cómodo"**. Está construido con FastAPI y una **arquitectura multi-agente**: un agente clasificador detecta la intención de cada mensaje y lo deriva al agente especializado que puede responderlo.

Los agentes usan **RAG (Retrieval-Augmented Generation)**: buscan la información relevante en una base vectorial **ChromaDB** y **GPT-4o** redacta la respuesta usando solo esos datos, para no inventar productos ni precios. Cada usuario tiene su propia **memoria de conversación**, así que el bot entiende preguntas de seguimiento como *"¿y de qué está hecho?"*.

## Tecnologías

| Tecnología | Uso |
|---|---|
| **FastAPI** + **Uvicorn** | API web asíncrona y servidor |
| **Pydantic** | Validación de las peticiones (`ChatRequest`, `ChatResponse`) |
| **LangChain** | Integración con el modelo, embeddings, división de textos, memoria y cadenas |
| **OpenAI GPT-4o** | Clasificación de mensajes y generación de respuestas |
| **OpenAI Embeddings** | Vectores para la búsqueda de muebles y del clasificador |
| **ChromaDB** | Base vectorial persistente para la búsqueda semántica |
| **HTML + JavaScript** | Interfaz de chat |

## Cómo funciona

```
Usuario ──► POST /chatt ──► QuestionEvaluator (clasifica)
                                   │
          ┌──────────────┬─────────┴──────┬──────────────────┐
          ▼              ▼                ▼                  ▼
   furniture-questions  frequent-     smalltalk-       assistant-
   (productos)          questions     questions        questions
                        (la tienda)   (saludos)        (asesor humano)
          │              │                │
          └──────► búsqueda en ChromaDB ──┘
                         │
                         ▼
          GPT-4o + instruction.txt del agente + memoria del usuario
                         │
                         ▼
                     Respuesta
```

1. **Clasificación:** `QuestionEvaluator` busca ejemplos de preguntas parecidas y le pide a GPT-4o una sola etiqueta. No usa memoria, para que cada mensaje se clasifique solo por su contenido.
2. **Derivación:** `sChatbot2.py` envía el mensaje al agente que corresponde. Si la etiqueta no es válida (pregunta no relacionada con la tienda), responde *"No tengo información sobre ese tema. ¿Puedo ayudarte en algo más?"*.
3. **Búsqueda (RAG):** el agente recupera de ChromaDB los fragmentos más parecidos a la pregunta.
4. **Respuesta:** `langchain_service.py` arma el prompt con el `instruction.txt` del agente, los fragmentos recuperados (`{Context}`) y la memoria de ese usuario, y llama a GPT-4o.

### Agentes

| Agente | Responde | Fuente de datos |
|---|---|---|
| `question-evaluator` | A qué agente derivar cada mensaje | `question_evaluator_data.json` |
| `furniture-questions` | Precio, materiales y características de los productos | `furniture_data.json` |
| `frequent-questions` | Horarios, ubicación, medios de pago, envíos, garantía, promociones, contacto | `store-information.txt` |
| `smalltalk-questions` | Saludos, agradecimientos y despedidas | `smalltalk.json` |
| `assistant-questions` | Deriva a un asesor humano | — |

**Derivación a un humano:** cuando el usuario no quedó conforme o pide hablar con una persona, el agente le indica que escriba *"Asesor humano"*. Si el mensaje contiene palabras como *humano* o *asesor*, responde directamente con el enlace de WhatsApp, sin llamar al modelo.

### Memoria de conversación

Cada agente guarda una memoria separada por `chat_id`. La interfaz genera un `chat_id` aleatorio por pestaña, así que cada usuario tiene su propio historial y nadie ve la conversación de otro.

```
You - 03:30 a. m.
cuanto cuesta el sofa minimalista?

Chatbot - 03:30 a. m.
El Sofá Minimalista cuesta 500 USD.

You - 03:31 a. m.
de que esta hecho?

Chatbot - 03:31 a. m.
El Sofá Minimalista está tapizado en tela de alta calidad, lo que le da una apariencia elegante y duradera. Su estructura está hecha de madera maciza, lo que asegura su resistencia y durabilidad. Los cojines están generosamente rellenos para proporcionar una comodidad inigualable.
```

## Instalación y ejecución

Requisitos: Python 3.13 y una API key de OpenAI con créditos.

1. **Instalar dependencias** (desde la carpeta `ChatBot-API`):
   ```
   cd ChatBot-API
   pip install -r requirements.txt
   ```

2. **Configurar la API key:** crear un archivo `.env` en la raíz del repositorio (está en `.gitignore`, nunca se sube):
   ```
   OPENAI_API_KEY=sk-...
   ```

3. **Cargar los datos** en ChromaDB (una vez, o cada vez que cambien los archivos de `app/services/data/`):
   ```
   python cargar_datos.py
   ```
   Se puede ejecutar las veces que se quiera: los datos se reemplazan, no se duplican.

4. **Iniciar el servidor** (desde `ChatBot-API`):
   ```
   python -m uvicorn app.main:app --reload --port 8002
   ```

5. Abrir el chat en **http://127.0.0.1:8002** o la documentación interactiva en **http://127.0.0.1:8002/docs**.

## API

### `POST /chatt`
Envía un mensaje al chatbot.

```json
{
  "chat_id": "123",
  "message": "cuanto sale la lampara de pie industrial?"
}
```

Respuesta:
```json
{
  "chat_id": "123",
  "response": "La Lámpara de Pie Industrial cuesta 120 USD."
}
```

### `POST /upload-data?layer=<capa>`
Carga en ChromaDB los datos de un agente. Capas válidas: `furniture-questions`, `frequent-questions`, `smalltalk-questions`, `question-evaluator`. Una capa inválida devuelve `400`. Es la alternativa a `cargar_datos.py` con el servidor encendido.

### `GET /`
Devuelve la interfaz de chat.

## Estructura del proyecto

```
CursoIAG-Chatbot/
├── .env                          # API key (no se sube a git)
├── README.md
└── ChatBot-API/
    ├── requirements.txt
    ├── cargar_datos.py           # Carga todas las bases de ChromaDB
    ├── chroma_db*/               # Bases vectoriales generadas (no se suben a git)
    └── app/
        ├── main.py               # App FastAPI, CORS y página principal
        ├── models/
        │   └── mChatbot.py       # ChatRequest, ChatResponse
        ├── routes/
        │   ├── chatbot2.py       # /chatt y /upload-data
        │   └── chatbot.py        # Versión 1 (no registrada)
        ├── services/
        │   ├── sChatbot2.py      # Orquestador: clasifica y deriva al agente
        │   ├── sChatbot.py       # Versión 1: una sola cadena RAG (referencia)
        │   ├── langchain_service.py  # Prompt + memoria + llamada a GPT-4o
        │   ├── data/             # Catálogo, información de la tienda y ejemplos
        │   └── agents/
        │       ├── base_agent.py # Clase base y memoria por chat_id
        │       ├── question_evaluator/
        │       ├── furniture_questions/
        │       ├── frequent_questions/
        │       ├── smalltalk_questions/
        │       └── assistant_questions/   # cada uno con su agente e instruction.txt
        └── static/
            └── index.html        # Interfaz de chat
```

`chatbot.py` y `sChatbot.py` son la primera versión del proyecto: una única cadena RAG con el catálogo escrito en el código. Se conservan como referencia, pero no se registran en `main.py` porque la versión multi-agente los reemplaza.

## Mejoras futuras

- Guardar la memoria en Redis o en una base de datos, con expiración, para que sobreviva a reinicios y funcione con varios servidores.
- Recortar el historial que se envía al modelo y no repetir el prompt del sistema en la memoria, para reducir costos.
- Usar `temperature=0` y salida estructurada en el clasificador para que siempre devuelva una etiqueta válida.
- Migrar `ConversationChain` y `ConversationBufferMemory` (obsoletos) a LCEL con `RunnableWithMessageHistory`.
- Autenticación en `/upload-data`, límite de peticiones y CORS restringido.
- Tests automáticos con el modelo simulado y un set de preguntas para medir la precisión del clasificador.
