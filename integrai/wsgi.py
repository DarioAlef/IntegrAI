#Web Server Gateway Interface – Interface de Porta de Entrada do Servidor 
# Web é uma especificação para uma interface simples e universal entre 
# servidores web e aplicações Web. O WSGI é um padrão que permite que os servidores web
# se comuniquem com aplicações web escritas em Python. Ele define como os servidores devem
# enviar solicitações para a aplicação e como a aplicação deve retornar respostas ao servidor.


"""
WSGI config for integrai project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'integrai.settings')

application = get_wsgi_application()
