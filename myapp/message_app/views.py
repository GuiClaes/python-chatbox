from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import MessageCreationForm, UserFinderForm
from .repository import MessageRepository
from login_app.repository import UserRepository

APP_NAME = "message-app"

def index(request, connected_user = "admin",  target_user = "Guillaume"):
    inbox_form = MessageCreationForm()
    user_finder_form = UserFinderForm()
    messages = MessageRepository.get_messages(connected_user, target_user)

    if "user_finder" in request.session:
        user_finder = request.session['user_finder']
        del request.session["user_finder"]
        target_message_list = MessageRepository.get_last_messages_for_targets(connected_user, user_finder)
    else:
        target_message_list = MessageRepository.get_targets_and_last_messages(connected_user)        

    return render(request, 'index.html', {'messages': messages, 'connected_user': connected_user, 'target_user': target_user, 'inbox_form': inbox_form, 'user_finder_form': user_finder_form, 'target_message_list': target_message_list})

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