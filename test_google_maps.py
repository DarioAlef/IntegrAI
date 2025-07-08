import sys
import os
import asyncio
sys.path.append('/home/thiago/projects/IntegrAI')

# Carrega as variáveis de ambiente
from dotenv import load_dotenv
load_dotenv()

from app.utils.google_maps import get_formatted_address

async def test_google_maps():
    print("🧪 Testando Google Maps API...")
    
    # Testa com alguns endereços
    test_locations = [
        "rua comendador matos areosa 481",
        "padaria em manaus",
        "shopping ponta negra manaus",
        "arena da amazônia manaus"
    ]
    
    for location in test_locations:
        print(f"\n{'='*50}")
        result = await get_formatted_address(location)
        print(f"📍 Resultado para '{location}': {result}")

if __name__ == "__main__":
    asyncio.run(test_google_maps())
