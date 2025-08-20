from pydantic import BaseModel
from typing import Optional

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
  
class PromptResponse(BaseModel):
  result: str
  tokens_used: int
  model: str