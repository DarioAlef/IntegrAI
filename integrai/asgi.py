#  Asynchronous Server Gateway Interface – Segue o mesmo raciocínio do WSGI 
# porém para tarefas assíncronas. O ASGI é uma especificação para aplicações web assíncronas
# e servidores web que suportam Python. Ele permite que aplicações web assíncronas
# se comuniquem com servidores web e vice-versa. O ASGI é uma evolução do WSGI,
# projetado para lidar com aplicações que exigem comunicação em tempo real, como WebSockets.


"""
ASGI config for integrai project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'integrai.settings')

application = get_asgi_application()
