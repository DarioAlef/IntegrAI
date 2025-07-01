# Módulo de Transcrição de Áudio

Este módulo contém todas as funcionalidades relacionadas ao processamento de áudio no IntegrAI.

## Estrutura dos Arquivos

### `audio_handler.py`
Módulo principal que centraliza toda a lógica de áudio movida do `webhook.py`. Contém:
- `detectar_audio_na_mensagem()`: Detecta se uma mensagem contém áudio
- `extrair_audio_data()`: Extrai dados de áudio de uma mensagem (base64 ou URL)
- `processar_deteccao_audio_webhook()`: Processa detecção de áudio no webhook
- `processar_audio_completo()`: Processa completamente um áudio (transcrição + resposta)

### `audio_transcription.py`
Contém funções específicas para transcrição de áudio:
- `convert_opus_to_wav()`: Converte áudio OPUS (WhatsApp) para WAV
- `transcrever_audio_groq()`: Transcreve áudio usando Groq/Whisper

### `audio_processing.py`
Arquivo legado que mantém compatibilidade com versões anteriores. Será depreciado em versões futuras.

## Uso

### No webhook.py:
```python
from app.services.transcription.audio_handler import processar_deteccao_audio_webhook, processar_audio_completo

# Detectar áudio
audio_data, tem_audio = processar_deteccao_audio_webhook(data)

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
