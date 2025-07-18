# Context - Gerenciamento de Contexto de Conversas

## 🧠 Visão Geral
Este módulo é responsável por manter e gerenciar o contexto de longo prazo das conversas, criando resumos inteligentes e atualizando perfis de usuário para conversas mais naturais e personalizadas.

## 🎯 Funcionalidades Principais
- **Resumo de Conversas**: Gera resumos concisos das interações
- **Perfil de Usuário**: Mantém dados atualizados sobre preferências e informações pessoais
- **Contextualização**: Preserva continuidade em conversas longas

## 📁 Estrutura de Arquivos

#### `context_storage.py`
- **Funcionalidade**: Coordena atualização e armazenamento de contexto
- **Regras de Negócio**:
  - Recebe histórico recente de mensagens
  - Integra contexto anterior com novas informações
  - Coordena geração de resumo via IA
  - Persiste contexto atualizado no banco de dados
  - Retorna contexto processado para uso imediato

#### `summary.py`
- **Funcionalidade**: Geração inteligente de resumos via IA
- **Regras de Negócio**:
  - Processa histórico de mensagens + contexto anterior
  - Gera resumo coerente de 500-700 caracteres
  - Extrai e atualiza dados do perfil do usuário
  - Retorna JSON estruturado com resumo e perfil
  - Utiliza modelo Groq para análise semântica

## 🔄 Fluxo de Processamento
1. **Recepção**: Histórico recente + contexto anterior
2. **Análise**: IA processa conversas para extrair insights
3. **Geração**: Criação de resumo e atualização de perfil
4. **Validação**: Extração e validação de JSON da resposta
5. **Persistência**: Armazenamento no banco via storage

## 📊 Estrutura do Contexto
```json
{
  "resumo": "string (500-700 caracteres)",
  "user_profile_data": {
    "nickname": "string",
    "cidade_atual": "string", 
    "aniversario": "date",
    "cpf": "string",
    "amigos": "array",
    // outros dados relevantes
  }
}
```

## 🔧 Dependências
- `groq`: Para processamento via IA
- `django`: Integração com modelos de banco
- `app.utils.validation`: Validação de JSON

## 🌐 Integração
- **Entrada**: User object + lista de mensagens + contexto anterior
- **Saída**: Contexto atualizado persistido
- **Modelos**: `User`, `DialogueContext` (Django)

## 📝 Características
- **Tamanho Otimizado**: Resumos mantidos entre 500-700 caracteres
- **Perfil Dinâmico**: Extração automática de dados pessoais
- **Processamento Assíncrono**: Operações não-bloqueantes
- **Validação Rigorosa**: JSON estruturado e validado
