from django.urls import path
from . import views

app_name = 'message_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('create', views.create_message, name='create'),
    path('find_user', views.find_user, name='find_user'),
    path('<str:target>/change_target', views.change_target, name='change_target')
]