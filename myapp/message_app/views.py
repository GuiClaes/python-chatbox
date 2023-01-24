from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Message
from .forms import MessageCreationForm
from .repository import MessageRepository
from datetime import datetime

APP_NAME = "message-app"

def index(request, message = MessageRepository.get_last_message()):
    messages = MessageRepository.get_messages()
    form = MessageCreationForm()
    return render(request, 'index.html', {'messages': messages, 'form': form, 'user_id': "admin", "message": message})

def get_message_details(request, message_id):
    message = MessageRepository.get_message(message_id)
    return index(request, message)

def get_messages(request):
    messages = Message.objects.order_by('-emission_time')
    return render(request, 'messages.html', {'messages': messages, 'user_id': "admin"})

def delete_message(request, message_id):
    message = MessageRepository.get_message(message_id)
    message.delete()
    return index(request)

def create_message(request):
    if request.method == 'GET':
        return index(request)
    elif request.method == 'POST':
        form = MessageCreationForm(request.POST)
        if form.is_valid():
            #Author should be provided with authentification
            Message(content = form.get_content(), emission_time = datetime.now(), author = form.get_author()).save()
            return HttpResponseRedirect('/'+APP_NAME)
    else:
        raise Exception("Request method not handled")