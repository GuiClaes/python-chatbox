from django.urls import path
from . import views

app_name = 'message_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('message', views.get_messages, name='messages'),
    path('message/<int:message_id>/details', views.get_message_details, name='message_details'),
    path('message/create', views.create_message, name='create'),
    path('message/<int:message_id>/delete', views.delete_message, name='delete')
]