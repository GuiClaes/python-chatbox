from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import RegisterForm, LoginForm
from .service import RegisterService

APP_NAME = "login-app"
USER_FINDER = "user_finder"
TARGET_USER = "target_user"
CURRENT_USER = "current_user"

def register(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})
    elif request.method == 'POST':
        form = RegisterForm(request.POST)
        service = RegisterService()
        if form.is_valid():
            service.register(username = form.get_username(), password = form.get_password(), email = form.get_email())
            return HttpResponseRedirect('/'+APP_NAME)
        else:
            return render(request, 'register.html', {'form': form, 'error_message': "Your registration is not valid."})   
    else:
        raise Exception("Request method not handled")

def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            service = RegisterService()
            if service.authenticate(username = form.get_username(), password = form.get_password()):
                request.session[CURRENT_USER] = crypt_session_attribute(form.get_username()) # We crypt username in session to avoid some client leaks
                return HttpResponseRedirect('/message-app')
            else:
                return render(request, 'login.html', {'form': form, 'error_message': "Log in failed, please verify your credential."})
    else:
        raise Exception("Request method not handled")

def logout(request):
    if CURRENT_USER in request.session:
        del request.session[CURRENT_USER]
    if USER_FINDER in request.session:
        del request.session[USER_FINDER]
    if TARGET_USER in request.session:
        del request.session[TARGET_USER]
    return HttpResponseRedirect('/' + APP_NAME)

#-----------------------------------------------------------------

def crypt_session_attribute(value:str):
    return "\_/".join(value)