import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
# chatbot (v1) no se registra: el frontend usa chatbot2, y v1 llama a OpenAI al arrancar
from app.routes import chatbot2

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chatbot2.router)

@app.get("/", response_class=HTMLResponse)
async def read_root():
    print("Current Directory:", os.getcwd())
    with open("./app/static/index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200) 