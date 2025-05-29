from langchain.agents import initialize_agent, Tool
from langchain.chat_models import ChatOpenAI
from app.services.openrouter import get_openrouter_response  # ajuste o import conforme sua estrutura
import os

# Define uma ferramenta para o agente LangChain usar o LLM
tools = [
    Tool(
        name="LlamaResponder",  # Nome da ferramenta
        func=get_openrouter_response,  # Função que será chamada
        description="Responde a comandos de linguagem natural"  # Descrição da ferramenta
    )
]

# Inicializa o agente LangChain com as ferramentas e o modelo de chat
agent = initialize_agent(
    tools, 
    ChatOpenAI(api_key=os.getenv("OPENROUTER_API_KEY")),  # Instancia o modelo de chat
    agent="zero-shot-react-description"  # Tipo de agente
)