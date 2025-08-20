from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from models import PromptRequest, PromptResponse
from services.github_models_service import github_models_service

# Carregar variáveis de ambiente (como o process.env. no Node.js)
load_dotenv()

# Criar instância da aplicação (como app = express() no Node.js)
app = FastAPI(
  title="My AI FullStack App",
  description="Aplicação de geração de texto com IA",
  version="1.0.0"
)

# Configurar CORS
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

@app.get("/")
async def root():
  """
  Rota de teste - equivalente a: 
  app.get('/', (req, res) => res.json({message: "Hello World"}))
  """
  return { "message": "FastAPI está funcionando" }

@app.get("/health")
async def health_check():
  return { "status": "healthy", "service": "my-ai-fullstack-app" }

@app.get("/models")
async def get_models_info():
  """
  Retorna informações sobre o modelo configurado no .env
  """
  return github_models_service.get_model_info()

@app.get("/models/current")
async def get_current_model():
  """
  Retorna apenas o modelo atualmente configurado
  """
  return {
    "current_model": github_models_service.get_current_model(),
    "endpoint": "GitHub Models"
  }

@app.post("/generate", response_model=PromptResponse)
async def generate_text(request: PromptRequest):
  """
  Rota para gerar texto usando GitHub Models - equivalente a:
  app.post('/generate', async (req, res) => {
    const result = await generateText(req.body.prompt);
    res.json(result);
  })
  """
  return github_models_service.generate_text(request)

@app.post("/chat")
async def chat_endpoint(request: PromptRequest):
  response = await github_models_service.generate_text(request)
  return {
    "message": response.result,
    "metadata": {
      "tokens_used": response.tokens_used,
      "model": response.model
    }
  }

