"""Organization admin interface."""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Organization, OrganizationMember


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = [
        'sid',
        'name',
        'archetype',
        'commitment',
        'member_count',
        'recruiting',
        'updated_at'
    ]
    list_filter = ['recruiting', 'archetype', 'commitment', 'primary_language']
    search_fields = ['sid', 'name', 'headline', 'description']
    readonly_fields = ['created_at', 'updated_at', 'api_data']

    fieldsets = (
        (_('Basic Information'), {
            'fields': ('sid', 'name', 'url')
        }),
        (_('Details'), {
            'fields': (
                'archetype',
                'commitment',
                'primary_language',
                'recruiting',
                'member_count'
            )
        }),
        (_('Description'), {
            'fields': ('headline', 'description', 'history', 'manifesto', 'charter'),
            'classes': ('collapse',)
        }),
        (_('Media'), {
            'fields': ('logo_url', 'banner_url'),
            'classes': ('collapse',)
        }),
        (_('API Data'), {
            'fields': ('api_data', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(OrganizationMember)
class OrganizationMemberAdmin(admin.ModelAdmin):
    list_display = [
        'handle',
        'display_name',
        'rank',
        'stars',
        'updated_at'
    ]
    list_filter = ['rank', 'stars']
    search_fields = ['handle', 'display_name', 'bio']
    readonly_fields = ['created_at', 'updated_at', 'api_data']
    ordering = ['-stars', 'handle']

    fieldsets = (
        (_('Basic Information'), {
            'fields': ('handle', 'display_name')
        }),
        (_('Organization Details'), {
            'fields': ('rank', 'stars')
        }),
        (_('Profile'), {
            'fields': ('avatar_url', 'bio'),
            'classes': ('collapse',)
        }),
        (_('API Data'), {
            'fields': ('api_data', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
