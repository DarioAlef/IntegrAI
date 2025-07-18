# Transcription - Transcrição de Áudio para Texto

## 🎙️ Visão Geral
Este módulo é responsável pela conversão de mensagens de áudio do WhatsApp em texto, utilizando a API Groq (Whisper) para transcrição precisa e rápida.

## 🎯 Funcionalidades Principais
- **Transcrição de Áudio**: Conversão de voz para texto
- **Conversão de Formato**: OPUS (WhatsApp) para WAV
- **Processamento em Memória**: Otimização sem arquivos temporários
- **Integração Whisper**: Utiliza modelo de IA avançado

## 📁 Estrutura de Arquivos

#### `audio_transcription.py`
- **Funcionalidade**: Motor completo de transcrição de áudio
- **Regras de Negócio**:

### 🔄 Conversão de Formato
- **`convert_opus_to_wav()`**: Converte OPUS para WAV
- Utiliza FFmpeg para conversão eficiente
- Processamento em memória (sem arquivos temporários)
- Entrada via pipe para otimização
- Saída preparada para APIs de transcrição

### 🎤 Transcrição via IA
- **`transcrever_audio_groq()`**: Transcreve áudio usando Groq
- Modelo Whisper para precisão máxima
- Suporte a múltiplos idiomas
- Processamento em tempo real
- Resposta em texto limpo

## 🔧 Dependências Técnicas
- **`groq`**: Cliente oficial da API Groq
- **`ffmpeg-python`**: Conversão de formatos de áudio
- **`io`**: Manipulação de streams em memória
- **`python-dotenv`**: Gerenciamento de configurações

## ⚙️ Configuração
### Variáveis de Ambiente:
- **`GROQ_API_KEY`**: Chave de autenticação da API Groq

### Dependências do Sistema:
- **FFmpeg**: Necessário para conversão de áudio
- **Codecs**: Suporte a OPUS e WAV

## 🔄 Fluxo de Processamento
1. **Recepção**: Áudio OPUS do WhatsApp
2. **Conversão**: OPUS → WAV via FFmpeg
3. **Preparação**: Stream em memória
4. **Transcrição**: Processamento via Groq/Whisper
5. **Retorno**: Texto transcrito limpo

## 📊 Formatos Suportados
### Entrada:
- **OPUS**: Formato padrão do WhatsApp
- **Outros**: Extensível para mais formatos

### Saída:
- **WAV**: Formato intermediário para transcrição
- **Texto**: Resultado final da transcrição

## 🚀 Otimizações
- **Memória**: Processamento sem arquivos temporários
- **Performance**: Conversão assíncrona via pipes
- **Qualidade**: Modelo Whisper de alta precisão
- **Velocidade**: Processamento em tempo real

## 🌐 Integração
- **Entrada**: Bytes de áudio do WhatsApp
- **Processamento**: FFmpeg + Groq/Whisper
- **Saída**: Texto transcrito para processamento

## 🛡️ Tratamento de Erros
- **Validação**: Verificação de formato de entrada
- **FFmpeg**: Tratamento de erros de conversão
- **API**: Gestão de falhas de transcrição
- **Fallback**: Estratégias de recuperação

## 📱 Casos de Uso
- **Comandos por Voz**: Interpretação de comandos falados
- **Conversas**: Transcrição para processamento de chat
- **Acessibilidade**: Conversão de áudio para texto
- **Logging**: Registro de mensagens de voz

## 📝 Características Especiais
- **Multilíngue**: Suporte automático a vários idiomas
- **Precisão**: Modelo Whisper state-of-the-art
- **Eficiência**: Processamento otimizado em memória
- **Integração**: Perfeita compatibilidade com WhatsApp

# Processar áudio completo
resposta = await processar_audio_completo(data, user, e, sender_number)
```

## Migração

A lógica de áudio foi movida do `webhook.py` para este módulo para:
1. Melhor organização do código
2. Separação de responsabilidades
3. Facilitar manutenção e testes
4. Reutilização de código

## Dependências

- `groq`: Para transcrição de áudio
- `ffmpeg`: Para conversão de formato de áudio
- `requests`: Para download de arquivos de áudio
- `base64`: Para decodificação de áudio em base64
