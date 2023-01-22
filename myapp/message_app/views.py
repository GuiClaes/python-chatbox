from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Message
from .forms import MessageCreationForm
from datetime import datetime

def get_message(request, message_id):
    message = get_object_or_404(Message, pk = message_id)
    return render(request, 'message.html', {'message': message})

def get_messages(request):
    messages = Message.objects.order_by('-emission_time')
    return render(request, 'messages.html', {'messages': messages})

def get_messages_form(request, form):
        messages = Message.objects.order_by('-emission_time')
        return render(request, 'messages.html', {'messages': messages, 'form': form})

def create_message(request):
    if request.method == 'GET':
        form = MessageCreationForm()
        return get_messages_form(request, form)

    elif request.method == 'POST':
        form = MessageCreationForm(request.POST)
        if form.is_valid():
            Message(content = form.get_content(), emission_time = datetime.now()).save()
            return HttpResponseRedirect('/message')

    return get_messages_form(request, form)
    #return render(request, 'message_form.html', {'form': form})