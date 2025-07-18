# User Management - Gerenciamento de Usuários

## 👤 Visão Geral
Este módulo é responsável pelo gerenciamento de usuários da aplicação IntegrAI, incluindo criação de novos usuários, validação de dados e integração com o sistema de contexto.

## 🎯 Funcionalidades Principais
- **Criação de Usuários**: Cadastro de novos usuários no sistema
- **Validação de Dados**: Verificação de informações de usuário
- **Inicialização**: Setup inicial de contexto para novos usuários
- **Integração**: Ponte entre autenticação e sistema principal

## 📁 Estrutura de Arquivos

#### `new_user.py`
- **Funcionalidade**: Processamento completo de cadastro de usuários
- **Regras de Negócio**:
  - Verificação automática de usuários existentes por número de telefone
  - Criação de registros via Django ORM
  - Inicialização de contexto vazio para novos usuários
  - Operações assíncronas para performance
  - Integração com sistema de armazenamento

## 🔄 Fluxo de Criação
1. **Recepção**: Número de telefone do usuário
2. **Verificação**: Checagem de existência no banco
3. **Criação**: Novo registro de usuário se necessário
4. **Inicialização**: Setup de contexto inicial
5. **Retorno**: Objeto User para uso imediato

## 🗄️ Estrutura de Dados
### Campos do Usuário:
- **`phone_number`**: Identificador único (número WhatsApp)
- **`name`**: Nome completo (opcional inicialmente)
- **`email`**: Email de contato (opcional inicialmente)
- **`waiting_user_data`**: Estado de coleta de dados
- **`waiting_event_data`**: Estado de processo de agendamento
- **`appointment_message_counter`**: Controle de etapas
- **`current_event_data`**: Dados temporários de evento

## 🔧 Dependências
- `django`: ORM e modelos
- `starlette.concurrency`: Operações assíncronas
- `core.models.User`: Modelo de dados principal
- `app.services.context.context_storage`: Sistema de contexto

## 🌐 Integração
- **Entrada**: Dados de webhook do WhatsApp
- **Processo**: Validação e criação no banco
- **Saída**: Objeto User configurado

## 📊 Estados de Usuário
### Estados Iniciais:
- **`waiting_user_data`**: `"waiting_for_name_and_email"`
- **`waiting_event_data`**: `None`
- **`appointment_message_counter`**: `0`

### Progressão:
1. **Novo**: Aguarda nome e email
2. **Autenticado**: Dados completos coletados
3. **Ativo**: Pronto para interações completas

## 🛡️ Validação e Segurança
- **Unicidade**: Número de telefone como chave única
- **Sanitização**: Limpeza de dados de entrada
- **Estados Controlados**: Progressão validada
- **Operações Atômicas**: Transações seguras

## 📱 Casos de Uso
- **Primeiro Acesso**: Usuário envia primeira mensagem
- **Autenticação**: Coleta de dados pessoais
- **Reativação**: Usuários que retornam ao sistema
- **Migração**: Transferência de dados entre versões

## 🚀 Performance
- **Async Operations**: Não bloqueia processamento
- **Lazy Loading**: Carregamento otimizado
- **Cache Ready**: Preparado para sistemas de cache
- **Batch Processing**: Suporte a operações em lote

## 📝 Características Especiais
- **Auto-Setup**: Configuração automática de dependências
- **Context Integration**: Inicialização de contexto
- **Error Handling**: Tratamento robusto de falhas
- **State Management**: Controle rigoroso de estados
