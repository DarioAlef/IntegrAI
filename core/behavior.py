# o arquivo behavior.py contém o comportamento da interação com o usuário, com funções que 
# controlam esse fluxo. Aqui você implementa a lógica de decisão: verificar se o usuário está
# cadastrado, qual o próximo passo, qual ação chamar, etc.
# Usa funções de actions.py para executar tarefas.
# Exemplo: check_user, funções que processam mensagens recebidas e decidem o que fazer.



from .models import User
from .actions import send_message, menu
from ..app.utils.validation import is_valid_name_and_email
from django.http import JsonResponse

def check_user(data):
    phone_number = data[0]
    message = data[1]
    try:
        user = User.objects.get(phone_number=phone_number)
        if user.waiting_data == "waiting_for_name_and_email":
            valid_data = is_valid_name_and_email(message)
            if valid_data:
                user.name = valid_data['name']
                user.email = valid_data['email']
                user.waiting_data = None
                user.save()
                send_message(phone_number, "Cadastro atualizado com sucesso!")
                return JsonResponse({'status': 'success'})
            else:
                send_message(phone_number, 'Formato inválido de dados. Tente novamente.')
                return JsonResponse({'status': 'error'})
        elif user.waiting_data == "waiting_for_edit":
            valid_data = is_valid_name_and_email(message)
            if valid_data:
                user.name = valid_data['name']
                user.email = valid_data['email']
                user.waiting_data = None
                user.save()
                send_message(phone_number, "Dados editados com sucesso!")
                return JsonResponse({'status': 'success'})
            else:
                send_message(phone_number, 'Formato inválido. Operação cancelada.')
                user.waiting_data = None
                user.save()
                return JsonResponse({'status': 'error'})
        elif user.waiting_data == "waiting_for_delete_confirmation":
            # Implemente a lógica de exclusão aqui
            pass
        elif user.waiting_data is None:
            return menu(user, message)
    except User.DoesNotExist:
        user = User(phone_number=phone_number, waiting_data="waiting_for_name_and_email")
        user.save()
        send_message(phone_number, "Ainda não te cadastramos. Por favor, envie seu nome e email, separados por uma vírgula.\n\nExemplo: Thiago, thsilva.developer@gmail.com")
        return JsonResponse({'registered': False, 'status': 'waiting_for_name_and_email'})