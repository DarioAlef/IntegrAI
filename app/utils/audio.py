import base64  # Para decodificar áudios em base64.
import requests # Para fazer requisições HTTP (ex: baixar arquivos de áudio).

def extrair_audio_data(msg_data):
    # Procura se tem áudio em msg_data (em base64 ou dentro do campo audioMessage).
    if audio_base64 := msg_data.get("base64") or msg_data.get("audioMessage", {}).get("audio"): 
        return base64.b64decode(audio_base64)
    if "audioMessage" in msg_data and "url" in msg_data["audioMessage"]:
        audio_url = msg_data["audioMessage"]["url"]
        audio_response = requests.get(audio_url)
        return audio_response.content
    return None