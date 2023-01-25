from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .forms import RegisterForm, LoginForm
from .models import Register, User

APP_NAME = "login-app"

def register(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})
    elif request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            print(form)
            exists = Register.objects.filter(username = form.get_username()).exists()
            Register(username = form.get_username_if_unique(exists), password = form.get_password()).save() #We should crypt password
            User(username = form.get_username(), email = form.get_email()).save()
            return HttpResponseRedirect('/'+APP_NAME+'/login')
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
            if Register.objects.filter(username = form.get_username(), password = form.get_password()).exists(): #Not safe at all :p
                return HttpResponseRedirect('/message-app')
        return render(request, 'login.html', {'form': form, 'error_message': "Log in failed, please verify your credential."})
    else:
        raise Exception("Request method not handled")

def get_user_details(request, user_id):
    user = get_object_or_404(User, pk = user_id)
    return render(request, 'user_details.html', {'user': user})