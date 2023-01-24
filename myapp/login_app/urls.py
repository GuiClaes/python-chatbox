from django.urls import path
from . import views

app_name = 'login_app'
urlpatterns = [
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('user/<str:user_id>/details', views.get_user_details, name='user_details')
]