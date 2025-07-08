import os
import requests
from typing import Optional
import urllib.parse

async def get_formatted_address(location: str) -> Optional[str]:
    """
    Busca o endereço formatado usando Google Maps Places API
    
    Args:
        location: Local a ser pesquisado
        
    Returns:
        String com endereço formatado ou None se não encontrar
    """
    try:
        # Pega a API key do .env
        api_key = os.getenv("GOOGLE_MAPS_API_KEY")
        if not api_key:
            print("❌ GOOGLE_MAPS_API_KEY não encontrada no .env")
            return None
        
        # Codifica a query para URL
        encoded_query = urllib.parse.quote(location)
        
        # Monta a URL da API
        url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={encoded_query}&key={api_key}"
        
        print(f"🔍 Buscando endereço para: '{location}'")
        print(f"📡 URL da requisição: {url}")
        
        # Faz a requisição
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        print(f"📥 Resposta da API: {data}")
        
        # Verifica se encontrou resultados
        if data.get("status") == "OK" and data.get("results"):
            formatted_address = data["results"][0].get("formatted_address")
            print(f"✅ Endereço encontrado: {formatted_address}")
            return formatted_address
        else:
            print(f"⚠️ Nenhum resultado encontrado. Status: {data.get('status')}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro na requisição para Google Maps API: {e}")
        return None
    except Exception as e:
        print(f"❌ Erro geral ao buscar endereço: {e}")
        return None
