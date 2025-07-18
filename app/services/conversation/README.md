# Conversation - Integração com WhatsApp via Evolution API

## 💬 Visão Geral
Este módulo gerencia toda a comunicação com o WhatsApp através da Evolution API, incluindo envio de mensagens, busca de contatos e gerenciamento de conversas.

## 🎯 Funcionalidades Principais
- **Envio de Mensagens**: Comunicação direta via WhatsApp
- **Gerenciamento de Contatos**: Busca e organização de lista de contatos
- **Integração Evolution API**: Interface completa com a API de WhatsApp

## 📁 Estrutura de Arquivos

#### `evolutionAPI.py`
- **Funcionalidade**: Cliente principal para comunicação com Evolution API
- **Regras de Negócio**:
  - Configuração automática via variáveis de ambiente
  - Envio de mensagens de texto com delay configurável
  - Headers de autenticação padronizados
  - Estrutura de payload otimizada para WhatsApp
  - Gerenciamento de instâncias e chaves de API

#### `contacts.py`
- **Funcionalidade**: Gerenciamento de contatos do WhatsApp
- **Regras de Negócio**:
  - Busca completa de contatos via Evolution API
  - Busca de números por nome de contato
  - Tratamento de diferentes formatos de resposta da API
  - Filtragem e processamento de listas de contatos
  - Debug integrado para troubleshooting

## 🔧 Configuração
### Variáveis de Ambiente Requeridas:
- `SERVER_URL`: URL do servidor Evolution API
- `INSTANCE`: Nome da instância WhatsApp
- `AUTHENTICATION_API_KEY`: Chave de autenticação

## 🌐 Endpoints Utilizados
- **Envio de Mensagens**: `/message/sendText/{instance}`
- **Busca de Contatos**: `/chat/findContacts/{instance}`

## 📝 Características da Comunicação
- **Delay Padrão**: 10ms entre mensagens
- **Formato**: Mensagens de texto (text/plain)
- **Autenticação**: API Key no header
- **Protocolo**: HTTP/HTTPS REST

## 🔄 Fluxo de Operações
1. **Inicialização**: Carregamento de configurações
2. **Autenticação**: Validação de credenciais
3. **Operação**: Envio de mensagem ou busca de contatos
4. **Resposta**: Processamento de retorno da API

## 🛡️ Tratamento de Erros
- Validação de status HTTP
- Logs detalhados para debug
- Fallback para diferentes formatos de resposta
- Exceções informativas para falhas de autenticação

## 📱 Integração WhatsApp
- **Formato de Números**: Padrão internacional sem símbolos
- **Tipos de Mensagem**: Texto simples
- **Instâncias**: Suporte a múltiplas instâncias WhatsApp
