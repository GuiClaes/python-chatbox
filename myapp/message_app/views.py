from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import MessageCreationForm, UserFinderForm
from .repository import MessageRepository
from login_app.repository import UserRepository

APP_NAME = "message-app"

def index(request, connected_user = "admin",  target_user = "Guillaume"):
    messageRepository = MessageRepository()
    inbox_form = MessageCreationForm()
    user_finder_form = UserFinderForm()
    messages = messageRepository.get_messages(author = connected_user, target = target_user)

    if "user_finder" in request.session:
        user_finder = request.session['user_finder']
        del request.session["user_finder"]
        user_message_list = messageRepository.get_target_last_message(connected_user, user_finder)
    else:
        user_message_list = messageRepository.get_targets_and_last_messages(user=connected_user)     

    unactive_targets = list(filter(lambda x: x.get_target() != target_user, user_message_list))
    active_target = next(filter(lambda x: x.get_target() == target_user, user_message_list))

    return render(request, 'index.html', {'messages': messages, 'connected_user': connected_user, 'inbox_form': inbox_form, 'user_finder_form': user_finder_form, 'active_target': active_target, 'unactive_targets': unactive_targets})

def create_message(request, connected_user = "admin",  target_user = "Guillaume"):
    if request.method == 'POST':
        form = MessageCreationForm(request.POST)
        if form.is_valid():
            MessageRepository.create_message(author = connected_user, target = target_user, content = form.get_content())
        return HttpResponseRedirect('/'+APP_NAME)
    else:
        raise Exception("Request method not handled")

def find_user(request):
    if request.method == 'POST':
        form = UserFinderForm(request.POST)
        usernames = UserRepository.find_user(form.get_user())
        request.session['user_finder'] = usernames
        return HttpResponseRedirect('/'+APP_NAME)