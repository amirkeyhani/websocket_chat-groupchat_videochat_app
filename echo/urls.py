from django.urls import path

from .views import index, echo_image, join_chat, new_message

app_name = 'echo'

urlpatterns = [
    path('', index, name='index'), 
    path('image/', echo_image, name='echo_image'), 
    path('chat/<str:username>/', join_chat, name='join_chat'), 
    path('chat/new/<str:username>/', new_message, name='new_message'),
]
