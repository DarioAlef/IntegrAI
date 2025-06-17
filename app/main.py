from fastapi import FastAPI           
from dotenv import load_dotenv    
import uvicorn                     

from app.routes import webhook        # Importa as rotas do webhook (endpoints da API)

load_dotenv()                         
app = FastAPI()                       # Cria a aplicação FastAPI
app.include_router(webhook.router)    # Adiciona as rotas do webhook à aplicação

# Este bloco só é executado se o arquivo for rodado diretamente (não importado)
if __name__ == "__main__": 
    uvicorn.run(
        "app.main:app",       # Caminho para a aplicação FastAPI
        host="0.0.0.0",       # Faz o servidor escutar em todas as interfaces de rede
        port=5000,            # Porta onde a API ficará disponível
        reload=True           # Habilita recarregamento automático ao salvar arquivos
    )