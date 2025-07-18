# Storage - Persistência de Dados

## 💾 Visão Geral
Este módulo é responsável por toda a persistência de dados da aplicação, gerenciando o armazenamento de mensagens, contextos, eventos e operações CRUD com o banco de dados Django.

## 🎯 Funcionalidades Principais
- **Armazenamento de Mensagens**: Persistência do histórico de conversas
- **Gerenciamento de Contexto**: Salvamento de resumos e perfis de usuário
- **Operações CRUD**: Criação, leitura, atualização e exclusão de dados
- **Consultas Otimizadas**: Recuperação eficiente de histórico

## 📁 Estrutura de Arquivos

#### `storage.py`
- **Funcionalidade**: Interface completa de persistência de dados
- **Regras de Negócio**:

### 📝 Armazenamento de Mensagens
- **`store_message()`**: Persiste mensagens individuais
- Registra sender, content, timestamp e tipo (voz/texto)
- Associa mensagens ao usuário específico
- Operação assíncrona para performance

### 🧠 Gerenciamento de Contexto  
- **`store_context()`**: Salva/atualiza contexto de diálogo
- Utiliza update_or_create para eficiência
- Mantém um contexto por usuário
- Estrutura JSON para flexibilidade

### 📊 Recuperação de Dados
- **`retrieve_history()`**: Busca histórico de mensagens
- Limite configurável de mensagens
- Ordenação cronológica
- Retorna count para controle de paginação

### 👤 Gerenciamento de Usuários
- **`create_user()`**: Criação de novos usuários
- **`update_user()`**: Atualização de dados do usuário
- **`delete_user()`**: Remoção de usuários
- Validação de dados obrigatórios

### 📅 Gerenciamento de Eventos
- **`store_event()`**: Persistência de eventos/agendamentos
- Associação com usuário criador
- Dados estruturados de evento
- Integração com Google Calendar

## 🔄 Padrões de Uso

### Operações Assíncronas
Todas as operações utilizam `run_in_threadpool` para compatibilidade entre Django (síncrono) e FastAPI (assíncrono).

### Tratamento de Dados
- Validação automática de tipos
- Relacionamentos ORM otimizados
- Transações seguras

## 🗄️ Modelos Django Utilizados
- **`User`**: Dados de usuários e estados
- **`Message`**: Histórico de mensagens
- **`DialogueContext`**: Contextos de longo prazo
- **`Event`**: Eventos e agendamentos

## 🔧 Dependências
- `django`: ORM e modelos
- `starlette.concurrency`: Operações assíncronas
- `core.models`: Modelos de dados

## 🌐 Integração
- **Entrada**: Dados estruturados dos handlers
- **Processamento**: Operações de banco de dados
- **Saída**: Confirmações e dados recuperados

## 📈 Otimizações
- **Queries Eficientes**: Uso de select_related e prefetch_related
- **Paginação**: Controle de volume de dados
- **Índices**: Otimização de consultas frequentes
- **Bulk Operations**: Para operações em lote

## 🛡️ Segurança e Integridade
- **Validação**: Dados validados antes da persistência
- **Transações**: Operações atômicas
- **Relacionamentos**: Integridade referencial
- **Logs**: Rastreamento de operações

## 📝 Características Especiais
- **Assíncrono**: Compatível com FastAPI
- **Flexível**: Estruturas JSON para dados dinâmicos
- **Escalável**: Preparado para grandes volumes
- **Confiável**: Tratamento robusto de erros
