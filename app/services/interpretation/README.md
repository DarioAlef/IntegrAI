# Interpretation - Interpretação Inteligente de Comandos

## 🔍 Visão Geral
Este módulo utiliza inteligência artificial para interpretar e classificar mensagens dos usuários, identificando comandos específicos e extraindo informações estruturadas para agendamentos e outras funcionalidades.

## 🎯 Funcionalidades Principais
- **Detecção de Comandos**: Identifica tipos de comando nas mensagens
- **Interpretação de Agendamentos**: Extrai dados estruturados para eventos
- **Processamento de Cancelamentos**: Detecta intenções de cancelamento
- **Análise Semântica**: Compreensão contextual de mensagens

## 📁 Estrutura de Arquivos

#### `command_interpretation.py`
- **Funcionalidade**: Classificação principal de comandos
- **Regras de Negócio**:
  - Identifica se mensagem contém comando válido
  - Classifica entre comandos disponíveis: "agendamento", "conversa"
  - Retorna estrutura JSON com tipo e confiança
  - Utiliza IA para análise semântica
  - Sistema de confiança para validação

#### `appointment_interpretation.py`
- **Funcionalidade**: Extração de dados para agendamentos
- **Regras de Negócio**:
  - Análise completa de mensagens sobre eventos
  - Extração de título, data, hora, local e descrição
  - Formatação automática para fuso -04:00 (America/Manaus)
  - Cálculo automático de horário de término (1h padrão)
  - Validação de dados obrigatórios
  - Geração de JSON estruturado para eventos

#### `utils_interpretation.py`
- **Funcionalidade**: Utilitários de interpretação
- **Regras de Negócio**:
  - Detecção de confirmações (sim/não)
  - Identificação de intenções de cancelamento
  - Análise de sentimentos para confirmações
  - Processamento de respostas de usuário

## 🔄 Fluxo de Interpretação
1. **Recepção**: Mensagem de texto do usuário
2. **Análise Primária**: Identificação do tipo de comando
3. **Processamento Específico**: Extração de dados conforme tipo
4. **Validação**: Verificação de completude e consistência
5. **Estruturação**: Retorno em formato JSON padronizado

## 📊 Estruturas de Retorno

### Comando Geral:
```json
{
  "is_command": boolean,
  "command_type": "agendamento|conversa",
  "confidence": float
}
```

### Agendamento:
```json
{
  "event_summary": "string",
  "event_start": "datetime",
  "event_end": "datetime", 
  "event_location": "string",
  "event_description": "string"
}
```

### Confirmação/Cancelamento:
```json
{
  "is_confirmation": "yes|no|unclear",
  "is_cancellation": "yes|no|unclear"
}
```

## 🔧 Dependências
- `groq`: Processamento via IA
- `python-dotenv`: Configurações
- `typing`: Tipagem Python

## 🌐 Integração
- **Entrada**: Mensagens de texto ou histórico de conversa
- **Saída**: Dados estruturados em JSON
- **IA**: Modelo Groq para análise semântica

## ⚙️ Configurações
- **Fuso Horário**: -04:00 (America/Manaus) por padrão
- **Duração Padrão**: 1 hora para eventos sem fim especificado
- **Modelo IA**: Configurado via variável GROQ_API_KEY

## 📝 Características Especiais
- **Análise Contextual**: Considera conversa completa
- **Flexibilidade**: Aceita diferentes formatos de entrada
- **Robustez**: Tratamento de dados incompletos
- **Localização**: Específico para contexto brasileiro
