from pydantic import BaseModel
import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

# Pydantic é como o Joi ou Zod no Node.js - validação de dados
class PromptRequest(BaseModel):
  """
  Modelo para requisição - equivalente a interface em TypeScript:
  interface PromptRequest {
    prompt: string;
    max_tokens?: number;
  }
  """
  prompt: str
  max_tokens: Optional[int] = 100
  model: Optional[str] = os.getenv("MODEL_NAME")
  temperature: Optional[float] = 0.7
  
class PromptResponse(BaseModel):
  result: str
  tokens_used: Optional[int] = None
  model: str
  provider: str = "GitHub Models"