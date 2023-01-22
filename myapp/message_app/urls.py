from django.urls import path
from . import views

app_name = 'message_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('message', views.get_messages, name='messages'),
    path('<int:message_id>', views.get_message, name='message'),
    path('create', views.create_message, name='create'),
    path('delete/<int:message_id>', views.delete_message, name='delete')
]