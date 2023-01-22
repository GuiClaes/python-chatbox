from django.urls import path
from . import views

app_name = 'message_app'
urlpatterns = [
    path('', views.get_messages, name='messages'),
    path('<int:message_id>', views.get_message, name='message'),
    path('create', views.create_message, name='create')
]