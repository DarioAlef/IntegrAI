# Chatbot - Motor de Inteligência Artificial

## 🤖 Visão Geral
Este módulo contém o núcleo da inteligência artificial da aplicação IntegrAI, responsável por gerar respostas contextualizadas através do modelo de linguagem da Groq.

## 🎯 Funcionalidades Principais
- **Geração de Respostas**: Processa mensagens do usuário e gera respostas inteligentes
- **Contextualização**: Utiliza histórico de conversas para manter contexto
- **Personalização**: Respostas adaptadas ao perfil e preferências do usuário

## 📁 Estrutura de Arquivos

#### `chatbot.py`
- **Funcionalidade**: Motor principal do chatbot com integração Groq
- **Regras de Negócio**:
  - Processamento de mensagens em formato de conversa
  - Integração com modelo `deepseek-r1-distill-llama-70b`
  - Contextualização automática com histórico anterior
  - Resposta sempre em português brasileiro
  - Controle de temperatura (criatividade) e tokens
  - Incorporação de data/hora atual nas respostas

## ⚙️ Configurações do Modelo
- **Modelo**: `deepseek-r1-distill-llama-70b`
- **Temperature**: 0.6 (equilibrio entre criatividade e consistência)
- **Max Tokens**: 2048
- **Top P**: 0.95
- **Streaming**: Desabilitado para respostas completas

## 🔧 Dependências
- `groq`: Cliente oficial da API Groq
- `python-dotenv`: Gerenciamento de variáveis de ambiente

## 🌐 Integração
- **Entrada**: Lista de mensagens formatadas + contexto opcional
- **Saída**: Resposta em texto natural português
- **Variáveis de Ambiente**: Requer `GROQ_API_KEY`

## 📝 Comportamento
- **Identidade**: Se apresenta como "IntegrAI"
- **Idioma**: Responde exclusivamente em português
- **Contexto**: Utiliza resumo de conversas anteriores
- **Temporalidade**: Incorpora data/hora atual para contexto temporal

## 🔒 Segurança
- Chave API protegida via variáveis de ambiente
- Validação de presença da chave antes de operações
- Tratamento de erros de autenticação
