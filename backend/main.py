from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

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

