"""
URL configuration for Farout Django project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.core import views as core_views

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Health check
    path('health/', core_views.health_check, name='health_check'),

    # Authentication (django-allauth)
    path('accounts/', include('allauth.urls')),

    # Core views
    path('', core_views.home, name='home'),
    path('dashboard/', core_views.dashboard, name='dashboard'),

    # TinyMCE
    path('tinymce/', include('tinymce.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Customize admin site
admin.site.site_header = 'Farout Administration'
admin.site.site_title = 'Farout Admin'
admin.site.index_title = 'Welcome to Farout Admin Portal'
