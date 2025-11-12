"""
URL configuration for organization app.
"""
from django.urls import path
from . import views

app_name = 'organization'

urlpatterns = [
    path('members/', views.MemberListView.as_view(), name='member_list'),
    path('members/<slug:handle>/', views.MemberDetailView.as_view(), name='member_detail'),
]
