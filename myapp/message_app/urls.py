from django.urls import path
from . import views

app_name = 'message_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('message', views.get_messages, name='messages'),
    path('message/details/<int:message_id>', views.get_message_details, name='message'),
    path('message/create', views.create_message, name='create'),
    path('message/delete/<int:message_id>', views.delete_message, name='delete')
]