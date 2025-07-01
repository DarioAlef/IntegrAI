# Inicializa o Django para permitir uso dos modelos fora do padrão Django.
import os
import django
from starlette.concurrency import run_in_threadpool
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'integrai.settings')
django.setup()

# Importa os modelos e funções utilitárias do projeto.
from app.services.storage.storage import create_user, delete_user, update_user
from core.models import User
from app.services.conversation.evolutionAPI import EvolutionAPI
from app.utils.validation import is_valid_name_and_email




async def authenticate(phone_number, message) -> User | None:  
    messenger = EvolutionAPI()
    try:
        # Use run_in_threadpool para operações síncronas do Django
        user = await run_in_threadpool(
            User.objects.get, 
            phone_number=phone_number
        )
        
        if user.waiting_user_data == "waiting_for_name_and_email":
            if valid_data := is_valid_name_and_email(message):
                try:
                    await update_user(user, valid_data['name'], valid_data['email'])
                except Exception as e:
                    await messenger.enviar_mensagem(f"Erro ao atualizar os dados: {str(e)}", phone_number)
                    print({'status': 'Error updating user data.'})
                    return

                # Se chegou aqui, update_user() foi bem-sucedido
                await messenger.enviar_mensagem("Cadastro feito com sucesso!", phone_number)
                await messenger.enviar_mensagem("Apresentacao_e_guia_de_uso[...]", phone_number)
                return
            else:
                await messenger.enviar_mensagem('Formato inválido de dados.\n\nPor favor, digite seu nome e email, separados por uma vírgula.\n\nExemplo: Thiago, thsilva.developer@gmail.com', phone_number)
                print ({'status': 'Invalid name and email. Waiting for new try.'})
                return 
        elif user.waiting_user_data == "waiting_for_edit":
            if valid_data := is_valid_name_and_email(message):
                try:
                    await update_user(user, valid_data['name'], valid_data['email'])
                except Exception as e:
                    await messenger.enviar_mensagem(f"Erro ao atualizar os dados: {str(e)}", phone_number)
                    print({'status': 'Error updating user data.'})
                    return

                # Se chegou aqui, update_user() foi bem-sucedido
                await messenger.enviar_mensagem("Cadastro feito com sucesso!", phone_number)
                await messenger.enviar_mensagem("Apresentacao_e_guia_de_uso[...]", phone_number)
                return
            else:
                await messenger.enviar_mensagem('Formato inválido. Operação cancelada.', phone_number)
                user.waiting_user_data = None
                await run_in_threadpool(user.save)
                print ({'status': 'Invalid name and email. End of process'})
                return
        elif user.waiting_user_data == "waiting_for_delete_confirmation":
            await run_in_threadpool(delete_user, user)
            return
        elif user.waiting_user_data is None:
            print ({'status': 'proceed'})
            return user
    except User.DoesNotExist:
        await create_user(phone_number)
        await messenger.enviar_mensagem("Ainda não te cadastramos. Para que eu possa te oferecer os meus serviços, por favor, digite seu nome e email, separados por uma vírgula.\n\nExemplo: Thiago, thsilva.developer@gmail.com", phone_number)
        return