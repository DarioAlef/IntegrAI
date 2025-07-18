# Mailing - Sistema de Envio de Mensagens

## 📧 Visão Geral
Este módulo processa comandos especiais para envio de mensagens para contatos específicos via WhatsApp, utilizando busca inteligente de contatos e integração com a Evolution API.

## 🎯 Funcionalidades Principais
- **Comando de Envio**: Processamento de comandos "enviar mensagem para..."
- **Busca de Contatos**: Localização automática de contatos por nome
- **Envio Automático**: Entrega de mensagens via WhatsApp

## 📁 Estrutura de Arquivos

#### `send_message_command.py`
- **Funcionalidade**: Processamento completo de comandos de envio
- **Regras de Negócio**:
  - Detecção via regex do padrão "enviar mensagem para [nome]: [mensagem]"
  - Extração automática de nome do destinatário e conteúdo
  - Busca inteligente de contatos na lista do usuário
  - Validação de existência do contato
  - Envio automático via Evolution API
  - Logs detalhados para troubleshooting

## 🔄 Fluxo de Processamento
1. **Detecção**: Regex identifica comando de envio
2. **Extração**: Nome do contato e mensagem são separados
3. **Busca**: Localização do número via lista de contatos
4. **Validação**: Confirmação de que o contato foi encontrado
5. **Envio**: Mensagem é enviada via WhatsApp
6. **Log**: Registro de todo o processo

## 📝 Formato de Comando
```
enviar mensagem para [NOME_DO_CONTATO]: [MENSAGEM]
```

### Exemplos:
- `enviar mensagem para João: Oi, como você está?`
- `enviar mensagem para Maria Silva: Reunião confirmada para amanhã`

## 🔧 Dependências
- `re`: Expressões regulares para parsing
- `os`: Variáveis de ambiente
- `app.services.conversation.contacts`: Gerenciamento de contatos
- `app.services.conversation.evolutionAPI`: Envio de mensagens

## 🌐 Integração
- **Entrada**: Comando de texto formatado
- **Processo**: Busca + validação + envio
- **Saída**: Mensagem entregue no WhatsApp

## ⚠️ Considerações
- **Case Insensitive**: Busca não diferencia maiúsculas/minúsculas
- **Busca Flexível**: Encontra contatos por nome parcial
- **Logs Extensivos**: Debug completo do processo
- **Validação Rigorosa**: Confirma existência antes do envio

## 🛡️ Tratamento de Erros
- Contato não encontrado: Log de erro detalhado
- Falha na busca: Exceções capturadas e registradas
- Problemas de envio: Logs de status da Evolution API

## 📱 Casos de Uso
- **Assistente Pessoal**: Envio rápido de mensagens
- **Automação**: Notificações programadas
- **Integração**: Ponte entre diferentes conversas
