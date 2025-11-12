"""URL patterns for squadron app."""
from django.urls import path
from . import views

app_name = 'squadron'

urlpatterns = [
    path('', views.squadron_list, name='squadron_list'),
    path('my/', views.my_squadron, name='my_squadron'),
    path('<slug:slug>/', views.squadron_detail, name='squadron_detail'),
]
