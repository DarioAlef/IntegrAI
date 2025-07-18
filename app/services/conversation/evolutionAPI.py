from dotenv import load_dotenv
import httpx
import os

load_dotenv()

# Classe que encapsula a lógica de envio de mensagens via Evolution API.
class EvolutionAPI():
    
    def __init__(self):
        # Construtor da classe para configurações futuras.
        self.server_url = os.getenv("SERVER_URL")
        self.instance = os.getenv("INSTANCE")
        self.instance_key = os.getenv("AUTHENTICATION_API_KEY")
        self.headers = {
            "apikey": self.instance_key,           
            "Content-Type": "application/json"
        }
        pass

    # Método para o bot enviar uma mensagem de texto via Evolution API.
    async def enviar_mensagem(self, message, sender_number):

        url = f"http://{self.server_url}/message/sendText/{self.instance}"

        # payload é o corpo da requisição, sua importância é enviar os dados necessários para a API.
        payload = {
            "number": sender_number,  
            "options": {
                "delay": 10,         
                "presence": "composing"  
            },
            "textMessage": {
                "text": message       
            },
            "isBotMessage": True
                    # "options": {
        #     "delay": 123,
        #     "presence": "composing",
        #     "linkPreview": True,
        #     "quoted": {
        #         "key": {
        #             "remoteJid": "<string>",
        #             "fromMe": True,
        #             "id": "<string>",
        #             "participant": "<string>"
        #         },
        #         "message": {"conversation": "<string>"}
        #     },
        #     "mentions": {
        #         "everyOne": True,
        #         "mentioned": ["<string>"]
        #     }
        # },      
        }

        

        # Envia a requisição POST para o Evolution API
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(url, json=payload, headers=self.headers)

        return response


    async def send_audio(self, arq_b64, sender_number):

        url = f"http://{self.server_url}/message/sendWhatsAppAudio/{self.instance}"

        payload = {
            "number": sender_number,
            # "options": {
            #     "delay": 123,
            #     "presence": "recording",
            #     "encoding": True
            # },
            "audioMessage": {"audio": arq_b64}
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=self.headers)

        print(response.text)

    async def send_media(self, arq_b64):
        url = f"http://{self.server_url}/message/sendMedia/{self.instance}"

        payload = {
            "number": "5592981147651",
            # "options": {
            #     "delay": 123,
            #     "presence": "composing"
            # },
            "mediaMessage": {
                "mediatype": "image",
                "fileName": "image.png",
                "caption": "teste",
                "media": arq_b64
            }
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=self.headers)

        print(response.text)