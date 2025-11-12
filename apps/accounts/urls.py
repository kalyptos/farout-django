"""URL patterns for accounts app."""
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('profile/picture/upload/', views.upload_profile_picture, name='upload_profile_picture'),
    path('profile/picture/remove/', views.remove_profile_picture, name='remove_profile_picture'),
]
