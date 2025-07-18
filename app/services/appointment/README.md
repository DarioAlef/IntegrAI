# Appointment - Gerenciamento de Agendamentos

## 📅 Visão Geral
Este módulo é responsável por gerenciar o sistema de agendamentos da aplicação IntegrAI, incluindo a integração com o Google Calendar para criação, visualização e gerenciamento de eventos.

## 🎯 Funcionalidades Principais
- **Integração com Google Calendar**: Criação e gerenciamento de eventos no calendário do usuário
- **Autenticação OAuth2**: Sistema seguro de autenticação com as APIs do Google
- **Processamento de eventos**: Validação e formatação de dados de agendamento

## 📁 Estrutura de Arquivos

### `/google_calendar/`
Contém todos os arquivos relacionados à integração com a API do Google Calendar.

#### `auth_google.py`
- **Funcionalidade**: Gerencia a autenticação OAuth2 com o Google
- **Regras de Negócio**: 
  - Implementa o fluxo de autenticação segura
  - Gerencia tokens de acesso e refresh tokens
  - Mantém as credenciais do usuário para acesso às APIs

#### `events_mgmt.py`
- **Funcionalidade**: Operações CRUD para eventos no Google Calendar
- **Regras de Negócio**:
  - Criação de eventos com data, hora e descrição
  - Formatação automática de datas para o fuso horário -04:00 (America/Manaus)
  - Validação de dados antes da criação do evento
  - Integração com endereços via Google Maps quando necessário
  - Tratamento de erros da API do Google

## 🔧 Dependências
- `google-auth`
- `google-auth-oauthlib` 
- `google-auth-httplib2`
- `google-api-python-client`

## 🌐 Integração
- **Entrada**: Recebe dados interpretados pelos módulos de `interpretation`
- **Saída**: Eventos criados no Google Calendar
- **Modelos**: Utiliza o modelo `Event` do Django para persistência local

## 📝 Notas Importantes
- Todos os eventos são criados no fuso horário padrão -04:00 (America/Manaus)
- Requer arquivo `credentials.json` para autenticação com Google
- Mantém tokens em `token.json` para sessões persistentes
