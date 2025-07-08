import sys
sys.path.append('/home/thiago/projects/IntegrAI')

from app.utils.validation import extrair_json_da_resposta

# O JSON que está falhando (exatamente como vem da LLM)
json_str = '''{
    "resumo": "O usuário Thiago conversou sobre a Copa do Mundo de Clubes da FIFA, discutiu os times brasileiros participantes (Flamengo, Corinthians, Fluminense e Palmeiras) e compartilhou experiências de madrugada enquanto programava. Além disso, ele mencionou estar se sentindo bem (chibata) e compartilhou gírias.",
    "user_profile_data": {
        "cpf": None,
        "amigos": None,
        "nickname": "Thiago",
        "aniversário": None,
        "cidade_atual": None,
        "gírias_salvas": ["chibata", "filé"],
        "times_futebol": ["Flamengo", "Corinthians", "Fluminense", "Palmeiras"],
        "experiências_programação": ["maratonas de código até a madrugada"],
        "sentimento_atual": "chibata"
    }
}'''

print("Testando a função extrair_json_da_resposta corrigida...")
resultado = extrair_json_da_resposta(json_str)
print("\nResultado:")
print(resultado)
print("\nSucesso!" if not resultado.get('error') else "Falhou!")
