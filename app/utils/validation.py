# O arquivo utils.py geralmente serve para armazenar funções utilitárias e auxiliares que 
# são usadas em diferentes partes do projeto, mas que não pertencem diretamente a modelos, 
# views ou ações específicas. Ele ajuda a organizar o código e evitar repetição.

def is_valid_name_and_email(message):
    if not message:
          return None
    try:
        name, email = [x.strip() for x in message.split(',')]
        if '@' in email and name:
            return {'name': name, 'email': email}
    except Exception:
        pass
    return None



def valid_user_message(message, from_me, user_authenticated):
                if message and not from_me and user_authenticated:
                    return True
                return False



from datetime import datetime, timedelta
from typing import Union
import re
import json

from app.utils.now import now

def validate_event_data(event_data: dict) -> tuple[dict, dict]:

    #0. Validar se o parâmetro 'event_data' é um dicionário
    if not isinstance(event_data, dict):
        raise ValueError("O parâmetro 'event_data' deve ser um dicionário.")

    current_event_data = {}
    invalid_params = {}



    # 1. Validar se 'event_summary' e 'event_start' existem
    if event_data.get('event_summary'):
        current_event_data['event_summary'] = event_data['event_summary']
    else:
        invalid_params['event_summary'] = 'Este campo é obrigatório.'

    if event_data.get('event_start'):
        try:
            start = datetime.fromisoformat(event_data['event_start'])
            # now já é um objeto datetime, não precisa converter
            actual_now = now
            if start >= actual_now:
                current_event_data['event_start'] = event_data['event_start']
            else:
                invalid_params['event_start'] = 'A data de início não pode estar no passado.'
        except ValueError:
            invalid_params['event_start'] = 'Formato de data inválido (use ISO 8601).'
    else:
        invalid_params['event_start'] = 'Este campo é obrigatório.'
        start = None  # Para evitar erro nas próximas validações
    # 2. Validar se 'event_end' não é antes de 'event_start'
    if event_data.get('event_end'):
        try:
            end = datetime.fromisoformat(event_data['event_end'])
            if start and end < start:
                invalid_params['event_end'] = 'A data de término não pode ser antes da data de início.'
            else:
                current_event_data['event_end'] = event_data['event_end']
        except ValueError:
            invalid_params['event_end'] = 'Formato de data inválido (use ISO 8601).'
    else:
        if start:
            # Se não houver event_end mas start for válido, define como +1 hora
            end = start + timedelta(hours=1)
            current_event_data['event_end'] = end.isoformat()
        else:
            invalid_params['event_end'] = 'Sem data de início, não é possível determinar a data de término.'

    # 3. Campos opcionais
    for key in ['description', 'location', 'attendees', 'reminders']:
        if key in event_data:
            current_event_data[key] = event_data[key]

    # 4. Validar visibility
    visibility = event_data.get('visibility', 'private')
    if visibility in ['private', 'public']:
        current_event_data['visibility'] = visibility
    else:
        invalid_params['visibility'] = "Valor inválido. Use 'private' ou 'public'."

    return current_event_data, invalid_params


def format_event_time(date_time_iso: str, time_zone: str = "America/Sao_Paulo") -> dict:
    """Formata a data/hora no formato esperado pela API Google Calendar"""
    return {
        "dateTime": date_time_iso,
        "timeZone": time_zone
    }


def extrair_json_da_resposta(resposta: Union[str, dict]) -> dict:
    # Se já for dict (como parece ser), não precisa fazer nada
    if isinstance(resposta, dict):
        return resposta

    if not isinstance(resposta, str):
        print("❌ Tipo inesperado em 'resposta':", type(resposta))
        return {"error": True}

    try:
        print("Resposta recebida para extrair:", resposta)

        # Remove blocos markdown se existirem
        resposta = re.sub(r'```json|```', '', resposta).strip()

        # Extrai o bloco JSON
        match = re.search(r'\{.*\}', resposta, re.DOTALL)
        if match:
            json_str = match.group()
            
            # Abordagem simples e direta: corrigir problemas comuns
            fixes = [
                # 1. Tenta parse direto
                (json_str, "Parse direto"),
                
                # 2. PRINCIPAL: Substitui None por null (problema do Python vs JSON)
                (json_str.replace(': None,', ': null,').replace(': None}', ': null}'), "Python None -> JSON null"),
                
                # 3. Fix específico para aspas problemáticas
                (json_str.replace('"de origem misteriosa"', 'de origem misteriosa'), "Fix específico aspas"),
                
                # 4. Remove todas as aspas duplas problemáticas no meio de frases
                (re.sub(r'([a-záêçõ]+)\s+"([^"]+)"\s+([a-záêçõ]+)', r'\1 \2 \3', json_str), "Remove aspas no meio"),
                
                # 5. Último recurso: remove quebras de linha e tenta
                (json_str.replace('\n', ' ').replace('  ', ' '), "Normaliza espaços"),
            ]
            
            for json_corrigido, descricao in fixes:
                try:
                    resultado = json.loads(json_corrigido)
                    print(f"✅ Sucesso com: {descricao}")
                    return resultado
                except json.JSONDecodeError as e:
                    print(f"⚠️ {descricao} falhou: {e}")
                    continue
            
            # Se nenhuma estratégia funcionou, retorna erro
            print("❌ Todas as estratégias falharam")
            return {"error": True}
        else:
            print("⚠️ Nenhum JSON encontrado na resposta.")
    except Exception as e:
        print("❌ Erro geral ao extrair JSON:", e)

    return {"error": True}


def extrair_campos_manual(json_str: str) -> dict:
    """Extrai campos JSON manualmente quando o parse falha"""
    try:
        resultado = {}
        
        # Extrai resumo (melhor regex para capturar texto com aspas)
        resumo_match = re.search(r'"resumo":\s*"([^"]*(?:\\"[^"]*)*)"', json_str)
        if resumo_match:
            resultado['resumo'] = resumo_match.group(1).replace('\\"', '"')
        
        # Extrai user_profile_data usando uma abordagem mais robusta
        profile_match = re.search(r'"user_profile_data":\s*(\{[^}]*\})', json_str, re.DOTALL)
        if profile_match:
            profile_str = profile_match.group(1)
            
            # Tenta fazer parse apenas do objeto profile_data
            try:
                import ast
                profile_data = ast.literal_eval(profile_str.replace('null', 'None'))
                resultado['user_profile_data'] = profile_data
            except:
                # Se falhar, extrai manualmente
                profile_data = {}
                
                # Extrai campos com regex mais específica
                fields = re.findall(r'"([^"]+)":\s*([^,\n}]+)', profile_str)
                for key, value in fields:
                    value = value.strip()
                    if value == 'null':
                        profile_data[key] = None
                    elif value.startswith('"') and value.endswith('"'):
                        profile_data[key] = value[1:-1]
                    elif value.startswith('[') and value.endswith(']'):
                        # Extrai lista
                        items = re.findall(r'"([^"]+)"', value)
                        profile_data[key] = items
                    else:
                        profile_data[key] = value
                
                resultado['user_profile_data'] = profile_data
        
        return resultado if resultado else {"error": True}
    except Exception as e:
        print("❌ Erro na extração manual:", e)
        return {"error": True}

