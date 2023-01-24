from .models import Message
from django.shortcuts import get_object_or_404

class MessageRepository():
    def get_messages():
        return Message.objects.order_by('-emission_time')

    def get_message(message_id):
        return get_object_or_404(Message, pk = message_id)

    def get_last_message():
        return Message.objects.order_by('-emission_time').last()