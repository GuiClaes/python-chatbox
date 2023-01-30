from .models import Message, Target_message
from datetime import datetime
from django.db.models import Q

class MessageService:
    def get_messages(self, author, target):
        return Message.objects.filter(author__in = [author, target], target__in = [target, author]).order_by('emission_time')

    def create_message(self, author, target, content):
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

        return list(map(lambda y: Target_message(y[0], y[1]), sorted(target_message.items(), key=lambda f:f[1].emission_time, reverse=True)))

    def get_targets_last_message(self, user, targets):        
        return [Target_message(target = q[0], message = q[1]) for q in map(lambda target : (target, self.get_last_message(user1 = user, user2 = target)), targets)]
        
    def get_last_message(self, user1, user2):
        return Message.objects.filter(author__in = [user1, user2], target__in = [user2, user1]).order_by('emission_time').last()

    def get_last_message_target(self, author):
        message = Message.objects.filter(Q(author = author) | Q(target = author)).order_by('emission_time').last()
        return message.get_target() if message.get_author() == author else message.get_author()
    
    def count_message_sent_by_username(self, username):
        return Message.objects.filter(author = username).count()

    def count_message_sent_to_username(self, username):
        return Message.objects.filter(target = username).count()