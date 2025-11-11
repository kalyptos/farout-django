"""
Admin configuration for Member model.
"""
from django.contrib import admin
from .models import Member


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    """Admin interface for organization members."""

    list_display = ('display_name', 'discord_id', 'rank', 'total_missions', 'total_trainings', 'created_at')
    list_filter = ('rank', 'created_at')
    search_fields = ('display_name', 'discord_id', 'bio')
    ordering = ('-created_at',)

    fieldsets = (
        ('Basic Information', {
            'fields': ('discord_id', 'display_name', 'bio', 'avatar_url')
        }),
        ('Organization Details', {
            'fields': ('rank',)
        }),
        ('Progress', {
            'fields': ('missions_completed', 'trainings_completed', 'stats'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('created_at', 'updated_at')

    def total_missions(self, obj):
        return obj.total_missions
    total_missions.short_description = 'Missions'

    def total_trainings(self, obj):
        return obj.total_trainings
    total_trainings.short_description = 'Trainings'
