# IntegrAI: Seu Assistente Pessoal Inteligente no WhatsApp
**LINK PARA A APRESENTAÇÃO DO PROJETO:** https://www.notion.so/IntegrAI-1f837eb15adc80968f9dcbb31a373469?pvs=4

## Visão Geral
IntegrAI é um assistente pessoal inteligente inspirado no conceito do Jarvis, do Homem de Ferro. Ele simplifica sua rotina automatizando tarefas diárias como gerenciamento de e-mails, agendamento de compromissos e controle de dispositivos IoT, tudo por meio de comandos de voz ou texto no WhatsApp.

## Como Rodar o Projeto

Siga estas instruções para configurar e executar o IntegrAI:

### Pré-requisitos

*   Python 3.x
*   [Docker](https://www.docker.com/) (opcional, mas recomendado para o Evolution API)
*   Uma conta no [OpenRouter](https://openrouter.ai/) para obter uma API Key.

### Configuração

1.  **Clone o repositório:**

    ```bash
    git clone <seu_repositorio>
    cd IntegrAI
    ```

2.  **Crie e ative um ambiente virtual:**

    ```bash
    python -m venv .venv
    source .venv/bin/activate   # Linux/macOS
    .venv\Scripts\activate.bat  # Windows
    ```

3.  **Instale as dependências:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure as variáveis de ambiente:**

    *   Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

        ```properties
        DB_ENGINE=django.db.backends.postgresql_psycopg2  # Ou outro banco de dados
        DB_NAME=
        DB_HOST=
        DB_PORT=
        DB_USER=
        DB_PASSWORD=

        SERVER_URL=      # URL do Evolution API
        INSTANCE=        # Nome da instância no Evolution API
        API_KEY=         # API Key do Evolution API

        OPENROUTER_API_KEY=  # Sua API Key do OpenRouter
        ```

5.  **Configure o Evolution API:**

    *   Se você não tiver o Evolution API rodando, pode usar o Docker Compose:

        ```bash
        cd api/evolution
        docker-compose up -d
        ```

    *   Configure o Evolution API para enviar as mensagens recebidas para o endpoint `http://localhost:5000/webhook`.

6.  **Execute o chatbot:**

    ```bash
    python chatbot.py
    ```

    O servidor Flask será iniciado na porta 5000.

### Teste

Envie uma mensagem para o número WhatsApp conectado ao Evolution API. O IntegrAI deve responder automaticamente.

## Detalhes Técnicos

### Arquitetura

O IntegrAI possui uma arquitetura modular baseada em microsserviços, composta pelas seguintes camadas:

*   **Camada de Entrada:** Recebe as mensagens do WhatsApp através do Evolution API.
*   **Camada de Processamento de Linguagem Natural:** Utiliza o OpenRouter para interpretar as mensagens e gerar respostas.
*   **Camada de Ação:** Envia as respostas de volta para o WhatsApp através do Evolution API.

### Tecnologias

*   **Linguagem de Programação:** Python
*   **Framework Web:** Flask
*   **API de WhatsApp:** Evolution API
*   **Modelo de Linguagem:** OpenRouter (meta-llama/llama-4-maverick:free)
*   **Banco de Dados:** Django com PostgreSQL (configurável)

### Módulos Principais

*   `chatbot.py`: Lógica principal do chatbot, incluindo a integração com o OpenRouter e o Evolution API.
*   `utils/evolutionAPI.py`: Classe para interagir com o Evolution API.
*   `core/`: Aplicação Django para gerenciar os modelos de dados e a lógica de negócios.
*   `core/models.py`: Definição dos modelos de dados (User, Message, etc.).
*   `core/behavior.py`: Lógica de controle do fluxo de interação com o usuário.
*   `core/actions.py`: Funções para executar ações específicas (enviar mensagem, mostrar menu, etc.).

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.