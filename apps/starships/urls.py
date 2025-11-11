"""Starships URL configuration."""
from django.urls import path
from . import views

app_name = 'starships'

urlpatterns = [
    path('', views.ShipListView.as_view(), name='ship_list'),
    path('<int:pk>/', views.ShipDetailView.as_view(), name='ship_detail'),
]
