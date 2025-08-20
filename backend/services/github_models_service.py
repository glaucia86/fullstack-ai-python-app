# backend/services/github_models_service.py
from openai import OpenAI
from fastapi import HTTPException
from config import settings
from models import PromptRequest, PromptResponse
import logging

# Configurar logging para debug
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GitHubModelsService:
    """
    Serviço para GitHub Models - equivalente a uma classe service no Node.js
    """
    
    def __init__(self):
        """
        Inicializar cliente OpenAI com endpoint customizado do GitHub
        Equivalente em JS seria:
        
        const client = new OpenAI({
            baseURL: "https://models.github.ai/inference",
            apiKey: process.env.GITHUB_TOKEN
        });
        """
        self.client = OpenAI(
            base_url=settings.github_models_endpoint,
            api_key=settings.github_models_token,
        )
        
        logger.info(f"Cliente GitHub Models inicializado com endpoint: {settings.github_models_endpoint}")
    
    async def generate_text(self, request: PromptRequest) -> PromptResponse:
        """
        Gerar texto usando GitHub Models
        
        Equivalente JavaScript/TypeScript:
        async function generateText(request: PromptRequest): Promise<PromptResponse> {
            const response = await client.chat.completions.create({...});
            return { result: response.choices[0].message.content };
        }
        """
        try:
            # Usar modelo padrão se não fornecido (resolve o erro de tipo None)
            model_to_use = request.model or settings.model_name
            
            logger.info(f"Gerando texto com modelo: {model_to_use}")
            
            # Chamada para GitHub Models (sintaxe idêntica à OpenAI)
            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "Você é um assistente útil e criativo. Responda sempre em português brasileiro."
                    },
                    {
                        "role": "user", 
                        "content": request.prompt
                    }
                ],
                model=model_to_use,  # Agora sempre será uma string, nunca None
                max_tokens=request.max_tokens,
                temperature=request.temperature,
                top_p=1.0
            )
            
            # Extrair resposta (proteger contra None)
            generated_text = response.choices[0].message.content or ""
            
            # GitHub Models pode ou não retornar usage info
            tokens_used = None
            if hasattr(response, 'usage') and response.usage:
                tokens_used = response.usage.total_tokens
            
            logger.info(f"Texto gerado com sucesso. Tokens: {tokens_used}")
            
            return PromptResponse(
                result=generated_text.strip(),
                tokens_used=tokens_used,
                model=model_to_use,  # Usar o modelo que foi efetivamente usado
                provider="GitHub Models"
            )
            
        except Exception as e:
            logger.error(f"Erro no GitHub Models: {str(e)}")
            
            # Tratamento de erro específico para GitHub Models
            if "rate_limit" in str(e).lower():
                raise HTTPException(
                    status_code=429,
                    detail="Rate limit atingido. Tente novamente em alguns minutos."
                )
            elif "authentication" in str(e).lower():
                raise HTTPException(
                    status_code=401,
                    detail="Token GitHub inválido. Verifique GITHUB_MODELS_TOKEN no .env"
                )
            else:
                raise HTTPException(
                    status_code=500,
                    detail=f"Erro no GitHub Models: {str(e)}"
                )
    
    def get_current_model(self) -> str:
        """
        Retorna o modelo atualmente configurado no .env
        """
        return settings.model_name
    
    def get_model_info(self) -> dict:
        """
        Retorna informações sobre o modelo configurado
        Totalmente baseado nas configurações do .env
        """
        return {
            "current_model": settings.model_name,
            "endpoint": settings.github_models_endpoint,
            "provider": "GitHub Models"
        }

# Instância singleton do serviço
github_models_service = GitHubModelsService()