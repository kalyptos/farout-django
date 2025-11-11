"""
Admin configuration for Member model.
"""
from django.contrib import admin
from .models import Member, ShipOwnership


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    """Admin interface for organization members."""

    list_display = ('display_name', 'discord_id', 'rank', 'role', 'squadron', 'total_missions', 'total_trainings', 'created_at')
    list_filter = ('rank', 'role', 'squadron', 'created_at')
    search_fields = ('display_name', 'discord_id', 'bio', 'squadron')
    ordering = ('-created_at',)

    fieldsets = (
        ('Basic Information', {
            'fields': ('discord_id', 'display_name', 'bio', 'avatar_url', 'profile_image')
        }),
        ('Organization Details', {
            'fields': ('rank', 'role', 'squadron')
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


@admin.register(ShipOwnership)
class ShipOwnershipAdmin(admin.ModelAdmin):
    """Admin interface for ship ownership."""

    list_display = ('member', 'ship', 'quantity', 'acquired_date')
    list_filter = ('acquired_date',)
    search_fields = ('member__display_name', 'ship__name', 'ship__manufacturer__name')
    ordering = ('-acquired_date',)
    autocomplete_fields = ['member', 'ship']

    fieldsets = (
        ('Ownership', {
            'fields': ('member', 'ship', 'quantity')
        }),
        ('Details', {
            'fields': ('notes', 'acquired_date'),
        }),
    )

    readonly_fields = ('acquired_date',)
