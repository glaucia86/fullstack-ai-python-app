import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
  """
  Classe de configurações - equivalente a ter um config.js
  """
  
  # GitHub Models configurações
  github_models_token: str = os.getenv("GITHUB_MODELS_TOKEN", "")
  github_models_endpoint: str = os.getenv("GITHUB_MODELS_ENDPOINT", "https://models.inference.ai.azure.com")
  model_name: str = os.getenv("MODEL_NAME", "openai/gpt-4o")
  port: int = int(os.getenv("PORT", 8000))
  
  # Validação simples
  def __post_init__(self): 
    if not self.github_models_token:
      raise ValueError("GITHUB_MODELS_TOKEN não encontrado no ambiente.")
    
settings = Settings()