"""URL patterns for communications app."""
from django.urls import path
from . import views

app_name = 'communications'

urlpatterns = [
    path('inbox/', views.message_inbox, name='inbox'),
    path('send/', views.message_send, name='send'),
]
