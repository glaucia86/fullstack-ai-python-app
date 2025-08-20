import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
  """
  Classe de configurações - equivalente a ter um config.js
  """
  openai_api_key: str = os.getenv("GITHUB_MODELS_TOKEN")
  port: int = int(os.getenv("PORT", 8000))
  
  # Validação simples
  def __post_init__(self): 
    if not self.openai_api_key:
      raise ValueError("GITHUB_MODELS_TOKEN não encontrado no ambiente.")
    
settings = Settings()