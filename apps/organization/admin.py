"""
Django admin configuration for Organization app.
"""
from django.contrib import admin
from django.utils.html import format_html
from typing import Any
from .models import Organization, OrganizationMember


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    """Admin interface for organizations."""

    list_display = (
        'name',
        'sid',
        'archetype',
        'commitment',
        'member_count',
        'last_synced'
    )
    list_filter = ('archetype', 'commitment', 'last_synced')
    search_fields = ('name', 'sid', 'description')
    readonly_fields = ('last_synced', 'created_at', 'rsi_link')
    ordering = ('name',)

    fieldsets = (
        ('Basic Information', {
            'fields': ('sid', 'name', 'archetype', 'commitment', 'description')
        }),
        ('Statistics', {
            'fields': ('member_count',)
        }),
        ('Media', {
            'fields': ('banner_url', 'logo_url', 'url', 'rsi_link')
        }),
        ('API Data', {
            'fields': ('api_data', 'last_synced', 'created_at'),
            'classes': ('collapse',)
        }),
    )

    def rsi_link(self, obj: Organization) -> str:
        """Display clickable RSI link.

        Args:
            obj: Organization instance

        Returns:
            str: HTML formatted link
        """
        return format_html(
            '<a href="{}" target="_blank">View on RSI →</a>',
            obj.rsi_url
        )

    rsi_link.short_description = 'RSI Profile'  # type: ignore


@admin.register(OrganizationMember)
class OrganizationMemberAdmin(admin.ModelAdmin):
    """Admin interface for organization members."""

    list_display = (
        'handle',
        'display_name',
        'organization',
        'rank',
        'stars',
        'is_linked_display',
        'last_synced'
    )
    list_filter = ('organization', 'stars', 'last_synced')
    search_fields = ('handle', 'display_name', 'rank')
    readonly_fields = ('last_synced', 'created_at', 'citizen_link')
    ordering = ('organization', '-stars', 'handle')
    autocomplete_fields = ['user']

    fieldsets = (
        ('Basic Information', {
            'fields': ('organization', 'handle', 'display_name', 'citizen_link')
        }),
        ('Organization Details', {
            'fields': ('rank', 'stars')
        }),
        ('User Linking', {
            'fields': ('user',),
            'description': 'Link this SC member to a Django user account'
        }),
        ('Media', {
            'fields': ('avatar_url',)
        }),
        ('API Data', {
            'fields': ('api_data', 'last_synced', 'created_at'),
            'classes': ('collapse',)
        }),
    )

    def is_linked_display(self, obj: OrganizationMember) -> str:
        """Display linked status with icon.

        Args:
            obj: OrganizationMember instance

        Returns:
            str: HTML formatted status
        """
        if obj.is_linked:
            return format_html(
                '<span style="color: green;">✓ Linked</span>'
            )
        return format_html(
            '<span style="color: gray;">○ Not Linked</span>'
        )

    is_linked_display.short_description = 'User Link'  # type: ignore

    def citizen_link(self, obj: OrganizationMember) -> str:
        """Display clickable citizen link.

        Args:
            obj: OrganizationMember instance

        Returns:
            str: HTML formatted link
        """
        return format_html(
            '<a href="{}" target="_blank">View Citizen Profile →</a>',
            obj.citizen_url
        )

    citizen_link.short_description = 'RSI Profile'  # type: ignore
