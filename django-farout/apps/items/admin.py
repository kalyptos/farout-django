"""
Admin configuration for Item model.
"""
from django.contrib import admin
from .models import Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    """Admin interface for items/inventory."""

    list_display = ('title', 'quantity', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    ordering = ('title',)

    fieldsets = (
        ('Item Details', {
            'fields': ('title', 'description', 'quantity', 'image_url')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('created_at', 'updated_at')
