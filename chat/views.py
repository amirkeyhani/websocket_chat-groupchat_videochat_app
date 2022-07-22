from django.shortcuts import render, redirect, HttpResponse
from .forms import UserRegisterForm
from .models import *
from django.urls import reverse

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from django.db.models import Q
import json

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password2')
            
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('chat:index')
                
            return redirect('login')
    else:
        form = UserRegisterForm()
        
    return render(request, 'register.html', {'form': form})

def index(request):
    return HttpResponse('Index Page')

@login_required
def chat_index(request):
    current_user = request.user
    return render(request, 'index.html', {
        'members': current_user.member_set.all()
    })
    
@login_required
def create_chat(request):
    current_user = request.user
    title = request.POST['group_name']
    chat = GroupChat.objects.create(creator_id=current_user.id, title=title)
    Member.objects.create(chat_id=chat.id, user_id=current_user.id)
    return redirect(
        reverse('chat:chat', args=[chat.unique_code])
    )

@login_required
def chat(request, chat_id):
    current_user = request.user
    try:
        chat = GroupChat.objects.get(unique_code=chat_id)
    except GroupChat.DoesNotExist:
        return render(request, '404.html')
    
    if request.method == 'GET':
        if Member.objects.filter(chat_id=chat.id, user_id=current_user.id).count() == 0:
            return render(request, 'join_chat.html', {'chatObject': chat})
        
        return render(request, 'chat.html', {
            'chatObject': chat, 
            'chat_id_json': mark_safe(json.dumps(chat.unique_code))})
    elif request.method == 'POST':
        Member.objects.create(chat_id=chat.id, user_id=current_user.id)
        
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'chat_{chat.unique_code}', 
            {
                'type': 'chat_activity', 
                'message': json.dumps({
                    'type': 'join', 
                    'username': current_user.username
                })
            }
        )
        
        return render(request, 'chat.html', {
            'chatObject': chat, 
            'chat_id_json': mark_safe(json.dumps(chat.unique_code))
        })
        
@login_required
def leave_chat(request, chat_id):
    current_user = request.user
    try:
        chat = GroupChat.objects.get(unique_code=chat_id)
    except GroupChat.DoesNotExist:
        return render(request, '404.html')
    
    if chat.creator_id == current_user.id:
        chat.delete()
        
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'chat{chat.unique_code}', 
            {
                'type': 'chat_activity', 
                'message': json.dumps({
                    'type': 'delete'
                })
            }
        )
        
    else:
        Member.objects.filter(chat_id=chat.id, user_id=current_user.id).delete()
        
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'chat_{chat.unique_code}', 
            {
                'type': 'chat_activity', 
                'message': json.dumps({
                    'type': 'leave', 
                    'username': current_user.username
                })
            }
        )
        
    return redirect('chat:index')

def video_chat(request):
    current_user = request.user
    call_logs = VideoThread.objects.filter(
        Q(caller_id=current_user.id) | Q(callee_id=current_user.id)
    ).order_by('-created_at')[:5]
    return render(request, 'video_chat.html', {'call_logs': call_logs})