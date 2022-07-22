from django.urls import path

from .views import *

app_name = 'chat'

urlpatterns = [
    path('', chat_index, name='index'), 
    path('create/', create_chat, name='create_chat'), 
    path('<str:chat_id>/', chat, name='chat'), 
    path('<str:chat_id>/leave/', leave_chat, name='leave_chat'),
]
