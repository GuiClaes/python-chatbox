from .models import Message, Target_message
from django.shortcuts import get_object_or_404
from datetime import datetime
from django.db.models import Q

class MessageRepository:

    def get_messages(self, author, target):
        return Message.objects.filter(author__in = [author, target], target__in = [target, author]).order_by('emission_time')

    def create_message(author, target, content):
        Message(author = author, target = target, content = content, emission_time = datetime.now()).save()
    
    def get_targets_and_last_messages(self, user):
        target_message = {} #Dictionnary with user as key and message as item
        messages = Message.objects.filter(Q(author = user) | Q(target = user))
        for message in messages:
            target = message.target if message.author == user else message.author
            if target in target_message:
                if message.emission_time > target_message[target].emission_time:
                    target_message[target] = message
            else:
                target_message[target] = message
        return list(map(lambda y: Target_message(y[0], y[1].content), sorted(target_message.items(), key=lambda f:f[1].emission_time, reverse=True)))

    def get_targets_last_message(self, user, targets):        
        targets_messages = []
        for target in targets:
            last_message = self.get_last_message(user1 = user, user2 = target)
            if last_message == None:
                targets_messages.append(Target_message(target, "No message sent to this user yet."))
            else:
                targets_messages.append(Target_message(target, last_message.get_content()))            
        return targets_messages
        
    def get_last_message(self, user1, user2):
        return Message.objects.filter(author__in = [user1, user2], target__in = [user2, user1]).order_by('emission_time').last()

    def get_last_message_target(self, author):
        message = Message.objects.filter(Q(author = author) | Q(target = author)).order_by('emission_time').last()
        if message.get_author() == author:
            return message.get_target()
        else:
            return message.get_author()
    
    def count_message_sent_by_username(self, username):
        return Message.objects.filter(author = username).count()

    def count_message_sent_to_username(self, username):
        return Message.objects.filter(target = username).count()