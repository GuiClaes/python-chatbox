from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import MessageCreationForm, UserFinderForm
from .repository import MessageRepository
from login_app.repository import UserRepository
from .models import Target_message

APP_NAME = "message-app"
USER_FINDER = "user_finder"
TARGET_USER = "target_user"
CURRENT_USER = "current_user"

def index(request):
    connected_user = verify_session(request)
    messageRepository = MessageRepository()
    inbox_form = MessageCreationForm()
    user_finder_form = UserFinderForm()

    user_message_list = find_requested_users(request) or messageRepository.get_targets_and_last_messages(user=connected_user)
    
    if not user_message_list:
        target_user = connected_user
        request.session[TARGET_USER] = target_user
    
    if TARGET_USER not in request.session:
        target_user = user_message_list[0].get_target()
        request.session[TARGET_USER] = target_user
    else:
        target_user = request.session[TARGET_USER]

    unactive_targets = list(filter(lambda x: x.get_target() != target_user, user_message_list))
    opt_active_target = list(filter(lambda x: x.get_target() == target_user, user_message_list))
    if opt_active_target:
        active_target = opt_active_target[0]
    else:
        active_target = Target_message(target_user, "No message sent yet.")
    
    messages = messageRepository.get_messages(author = connected_user, target = target_user)

    return render(request, 'index.html', {'messages': messages, 'connected_user': connected_user, 'inbox_form': inbox_form, 'user_finder_form': user_finder_form, 'active_target': active_target, 'unactive_targets': unactive_targets})

def create_message(request):
    connected_user = verify_session(request)
    if request.method == 'POST':
        form = MessageCreationForm(request.POST)
        if form.is_valid():
            target_user = request.session[TARGET_USER]
            MessageRepository.create_message(author = connected_user, target = target_user, content = form.get_content())
        return HttpResponseRedirect('/'+APP_NAME)
    else:
        raise Exception("Request method not handled")

def find_user(request):
    if request.method == 'POST':
        form = UserFinderForm(request.POST)
        usernames = UserRepository.find_user(form.get_user())
        request.session[USER_FINDER] = usernames
        return HttpResponseRedirect('/'+APP_NAME)

def change_target(request, target):
    request.session[TARGET_USER] = target
    return HttpResponseRedirect('/'+APP_NAME)

#----------------------------------------------------------------------------------

def verify_session(request):
    if CURRENT_USER in request.session:
        return request.session[CURRENT_USER]
    else:
        return HttpResponseRedirect('/'+"login-app")

def find_requested_users(request):
    connected_user = verify_session(request)
    messageRepository = MessageRepository()
    if USER_FINDER in request.session:
        user_finder = request.session[USER_FINDER]
        del request.session[USER_FINDER]
        return messageRepository.get_targets_last_message(connected_user, user_finder)
    else:
        return []