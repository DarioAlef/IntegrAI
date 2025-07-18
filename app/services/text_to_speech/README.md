# Text to Speech - Conversão de Texto em Áudio

## 🔊 Visão Geral
Este módulo é responsável pela conversão de texto em áudio utilizando a API da Unreal Speech, permitindo que o sistema IntegrAI forneça respostas em formato de áudio para os usuários.

## 🎯 Funcionalidades Principais
- **Síntese de Voz**: Conversão de texto para áudio de alta qualidade
- **Integração API**: Comunicação com serviço Unreal Speech
- **Configuração Flexível**: Personalização via variáveis de ambiente

## 📁 Estrutura de Arquivos

#### `api_text_to_speech.py`
- **Funcionalidade**: Interface com a API Unreal Speech
- **Regras de Negócio**:
  - Carregamento de configurações via settings
  - Autenticação automática com API key
  - Preparação de requests para síntese de voz
  - Configuração de parâmetros de áudio
  - Integração com sistema de configuração global

## ⚙️ Configuração
### Variáveis de Ambiente:
- **`UNREAL_SPEECH_API_KEY`**: Chave de autenticação da API

### Características do Serviço:
- **Qualidade**: Áudio de alta qualidade
- **Velocidade**: Processamento rápido
- **Idiomas**: Suporte multilíngue
- **Vozes**: Múltiplas opções de voz

## 🔧 Dependências
- `app.utils.config`: Sistema de configuração centralizado
- Unreal Speech API (externa)

## 🌐 Integração
- **Entrada**: Texto para conversão
- **Processamento**: API Unreal Speech
- **Saída**: Arquivo de áudio processado

## 🔄 Fluxo de Operação
1. **Configuração**: Carregamento de API key
2. **Preparação**: Formatação do texto
3. **Requisição**: Envio para Unreal Speech
4. **Processamento**: Conversão texto → áudio
5. **Retorno**: Arquivo de áudio gerado

## 📝 Casos de Uso
- **Acessibilidade**: Respostas em áudio para usuários
- **Multimídia**: Enriquecimento de conversas
- **Conveniência**: Áudio para situações hands-free

## 🛡️ Segurança
- **API Key**: Protegida via variáveis de ambiente
- **Validação**: Verificação de autenticação
- **Controle**: Acesso controlado ao serviço

## 📱 Compatibilidade
- **WhatsApp**: Formato compatível com áudio do WhatsApp
- **Qualidade**: Otimizado para mensagens móveis
- **Tamanho**: Arquivos otimizados para envio

## 🚀 Performance
- **Cache**: Possibilidade de cache de áudios frequentes
- **Streaming**: Processamento em tempo real
- **Otimização**: Configurações para melhor performance
