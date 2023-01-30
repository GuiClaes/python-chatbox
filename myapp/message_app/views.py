from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import MessageCreationForm, UserFinderForm
from .service import MessageService
from login_app.service import UserService
from .models import Target_message

APP_NAME = "message-app"
USER_FINDER = "user_finder"
TARGET_USER = "target_user"
CURRENT_USER = "current_user"

def index(request):
    if verify_session(request):
        connected_user = get_session_or_die(request)
    else:
        return HttpResponseRedirect('/login-app')
        
    message_service = MessageService()
    inbox_form = MessageCreationForm()
    user_finder_form = UserFinderForm()

    user_message_list = find_requested_users(request) or message_service.get_targets_and_last_messages(user=connected_user)

    if TARGET_USER not in request.session:
        if(len(user_message_list) == 0):
            target_user = connected_user
        else:
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
    
    messages = message_service.get_messages(author = connected_user, target = target_user)

    return render(request, 'index.html', {'messages': messages, 'connected_user': connected_user, 'inbox_form': inbox_form, 'user_finder_form': user_finder_form, 'active_target': active_target, 'unactive_targets': unactive_targets})

def create_message(request):
    if verify_session(request):
        connected_user = get_session_or_die(request)
    else:
        return HttpResponseRedirect('/login-app')
    if request.method == 'POST':
        form = MessageCreationForm(request.POST)
        if form.is_valid():
            service = MessageService()
            target_user = request.session[TARGET_USER]
            service.create_message(author = connected_user, target = target_user, content = form.get_content())
        return HttpResponseRedirect('/'+APP_NAME)
    else:
        raise Exception("Request method not handled")

def find_user(request):
    if request.method == 'POST':
        form = UserFinderForm(request.POST)
        service = UserService()
        usernames = service.find_user(start = form.get_user())
        request.session[USER_FINDER] = usernames
        return HttpResponseRedirect('/'+APP_NAME)

def change_target(request, target):
    request.session[TARGET_USER] = target
    return HttpResponseRedirect('/'+APP_NAME)


def get_user_details(request):
    if verify_session(request):
        username = get_session_or_die(request)
    else:
        return HttpResponseRedirect('/login-app')
    user_service = UserService()
    user = user_service.find_user_by_username(username)
    message_service = MessageService()
    nb_messages_sent = message_service.count_message_sent_by_username(username = username)
    nb_messages_recieved = message_service.count_message_sent_to_username(username = username)
    return render(request, 'user_d.html', {'user': user, 'nb_messages_sent': nb_messages_sent, 'nb_messages_recieved': nb_messages_recieved})

#----------------------------------------------------------------------------------

def verify_session(request):
    return CURRENT_USER in request.session

def get_session_or_die(request):
    if CURRENT_USER in request.session:
        return decrypt_session_attribute(request.session[CURRENT_USER])
    else:
        raise Exception("No session found.")

def find_requested_users(request):
    if verify_session(request):
        connected_user = get_session_or_die(request)
    message_service = MessageService()
    if USER_FINDER in request.session:
        user_finder = request.session[USER_FINDER]
        del request.session[USER_FINDER]
        return message_service.get_targets_last_message(user = connected_user, targets = user_finder)
    else:
        return []

def decrypt_session_attribute(value:bytes):
    return value.replace("\_/", "")