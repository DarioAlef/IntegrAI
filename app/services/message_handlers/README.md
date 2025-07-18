# Message Handlers - Processamento Central de Mensagens

## 🔄 Visão Geral
Este módulo é o núcleo do processamento de mensagens da aplicação, coordenando autenticação, detecção de tipo de conteúdo, interpretação de comandos e roteamento para handlers especializados.

## 🎯 Funcionalidades Principais
- **Autenticação de Usuários**: Validação e criação de usuários
- **Detecção de Tipo**: Identifica áudio, texto ou comandos
- **Roteamento Inteligente**: Direciona para handlers apropriados
- **Processamento de Contexto**: Gerencia estado de conversação

## 📁 Estrutura de Arquivos

#### `authentication.py`
- **Funcionalidade**: Sistema de autenticação e cadastro de usuários
- **Regras de Negócio**:
  - Verificação automática de usuários existentes
  - Fluxo de cadastro para novos usuários
  - Validação de nome e email
  - Estados de espera para dados do usuário
  - Integração com banco de dados Django

#### `chatbot_handler.py`
- **Funcionalidade**: Processamento de conversas normais via IA
- **Regras de Negócio**:
  - Recuperação de histórico de mensagens (últimas 10)
  - Gerenciamento de contexto de longo prazo
  - Integração com motor de IA do chatbot
  - Divisão de mensagens longas para WhatsApp
  - Remoção de tags especiais da resposta

#### `context_handler.py`
- **Funcionalidade**: Gerenciamento de contexto de conversação
- **Regras de Negócio**:
  - Controle de frequência de atualização de contexto
  - Integração com sistema de resumos
  - Otimização de performance
  - Manutenção de estado de diálogo

#### `is_audio_handler.py`
- **Funcionalidade**: Detecção e processamento de mensagens de áudio
- **Regras de Negócio**:
  - Identificação de conteúdo de áudio
  - Roteamento para transcrição
  - Validação de formatos suportados

#### `is_command_handler.py`
- **Funcionalidade**: Orquestração de comandos especiais
- **Regras de Negócio**:
  - Verificação de processos em andamento
  - Detecção de cancelamentos
  - Roteamento para handlers específicos (agendamento, etc.)
  - Interpretação de comandos via IA

#### `is_text_handler.py`
- **Funcionalidade**: Processamento de mensagens de texto
- **Regras de Negócio**:
  - Identificação de tipo de conteúdo textual
  - Roteamento para chat ou comandos
  - Validação de entrada

## 📁 Subpasta: `/command_handlers/`

#### `appointment_handler.py`
- **Funcionalidade**: Processamento completo de agendamentos
- **Regras de Negócio**:
  - Fluxo multi-etapa de criação de eventos
  - Coleta incremental de dados
  - Validação via IA e regras de negócio
  - Confirmação antes da criação
  - Integração com Google Calendar
  - Estados de progresso do usuário

#### `cancel_handler.py`
- **Funcionalidade**: Cancelamento de processos em andamento
- **Regras de Negócio**:
  - Reset de estados de usuário
  - Limpeza de dados temporários
  - Confirmação de cancelamento
  - Restauração de estado normal

#### `mailing_handler.py`
- **Funcionalidade**: Processamento de comandos de envio de mensagem
- **Regras de Negócio**:
  - Integração com sistema de mailing
  - Busca de contatos
  - Validação de destinatários

## 🔄 Fluxo Principal
1. **Autenticação**: Verificação/criação de usuário
2. **Detecção de Tipo**: Áudio, texto ou comando
3. **Roteamento**: Direcionamento para handler apropriado
4. **Processamento**: Execução da lógica específica
5. **Resposta**: Envio de retorno via WhatsApp

## 🔧 Dependências
- `django`: Modelos e ORM
- `starlette.concurrency`: Operações assíncronas
- `re`: Processamento de texto
- Vários módulos internos da aplicação

## 🌐 Integração
- **Entrada**: Webhooks do WhatsApp via Evolution API
- **Processamento**: Múltiplos handlers especializados
- **Saída**: Respostas via WhatsApp ou ações no sistema

## 📊 Estados de Usuário
- `waiting_for_name_and_email`: Aguardando dados de cadastro
- `waiting_for_event_data`: Coletando dados de agendamento
- `appointment_message_counter`: Controle de etapas

## 🛡️ Características de Segurança
- Validação rigorosa de entrada
- Estados controlados de usuário
- Timeout automático de processos
- Logs detalhados para auditoria
