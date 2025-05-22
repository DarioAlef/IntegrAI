from rest_framework import routers
from core import views 

router = routers.DefaultRouter()
router.register('user', views.UserViewSet)
router.register('message', views.MessageViewSet)
router.register('dialogue-context', views.DialogueContextViewSet)
router.register('audio', views.AudioViewSet)