from .models import Message, Target_message
from django.shortcuts import get_object_or_404
from datetime import datetime

class MessageRepository():
    def get_messages(author, target):
        return Message.objects.filter(author__in = [author, target], target__in = [target, author]).order_by('emission_time')

    def create_message(author, target, content):
        Message(author = author, target = target, content = content, emission_time = datetime.now()).save()
    
    def get_targets_and_last_messages(user):
        sent_message_targets = {q.get_target() for q in Message.objects.filter(author = user).order_by('emission_time')}
        recieved_message_author = {q.get_author() for q in Message.objects.filter(target = user).order_by('emission_time')}
        sent_message_targets.update(recieved_message_author)

        l = []
        for target in sent_message_targets:
            last_message = get_last_message(user, target)
            l.append(Target_message(target, last_message.get_content()))
        return l
    
    def get_last_messages_for_targets(user, targets):
        l = []
        for target in targets:
            last_message = get_last_message(user, target)
            if last_message != None:
                l.append(Target_message(target, last_message.get_content()))
            else:
                l.append(Target_message(target, "No message sent to this user yet."))
        return l
        

def get_last_message(user1, user2):
    return Message.objects.filter(author__in = [user1, user2], target__in = [user2, user1]).order_by('emission_time').last()