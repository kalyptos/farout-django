"""
Django admin configuration for Starships app.
"""
from django.contrib import admin
from django.utils.html import format_html
from typing import Any
from .models import Manufacturer, Ship, ShipComponent


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    """Admin interface for ship manufacturers."""

    list_display = ('name', 'code', 'ship_count', 'last_updated')
    list_filter = ('last_updated', 'created_at')
    search_fields = ('name', 'code', 'description')
    readonly_fields = ('last_updated', 'created_at')
    ordering = ('name',)

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'code', 'description')
        }),
        ('Media', {
            'fields': ('logo_url',)
        }),
        ('API Data', {
            'fields': ('api_data', 'last_updated', 'created_at'),
            'classes': ('collapse',)
        }),
    )

    def ship_count(self, obj: Manufacturer) -> int:
        """Display number of ships for this manufacturer.

        Args:
            obj: Manufacturer instance

        Returns:
            int: Number of ships
        """
        return obj.ships.count()

    ship_count.short_description = 'Ships'  # type: ignore


class ShipComponentInline(admin.TabularInline):
    """Inline admin for ship components."""

    model = ShipComponent
    extra = 0
    fields = ('type', 'name', 'size', 'quantity')


@admin.register(Ship)
class ShipAdmin(admin.ModelAdmin):
    """Admin interface for ships."""

    list_display = (
        'name',
        'manufacturer',
        'type',
        'size',
        'status_badge',
        'crew_range',
        'cargo_capacity',
        'price',
        'last_updated'
    )
    list_filter = (
        'is_flight_ready',
        'is_concept',
        'size',
        'type',
        'manufacturer',
        'last_updated'
    )
    search_fields = ('name', 'model', 'description', 'manufacturer__name')
    readonly_fields = ('last_updated', 'created_at', 'status_badge')
    ordering = ('manufacturer__name', 'name')
    inlines = [ShipComponentInline]

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'manufacturer', 'model', 'type', 'size', 'focus', 'description')
        }),
        ('Physical Specifications', {
            'fields': ('length', 'beam', 'height', 'mass'),
            'classes': ('collapse',)
        }),
        ('Crew & Capacity', {
            'fields': ('crew_min', 'crew_max', 'cargo_capacity')
        }),
        ('Performance', {
            'fields': ('max_speed', 'price')
        }),
        ('Media', {
            'fields': ('image_url', 'store_url')
        }),
        ('Status', {
            'fields': ('is_flight_ready', 'is_concept', 'status_badge')
        }),
        ('API Data', {
            'fields': ('api_data', 'last_updated', 'created_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['mark_flight_ready', 'mark_concept']

    def status_badge(self, obj: Ship) -> str:
        """Display colored status badge.

        Args:
            obj: Ship instance

        Returns:
            str: HTML formatted status badge
        """
        if obj.is_flight_ready:
            color = 'green'
            status = 'Flight Ready'
        elif obj.is_concept:
            color = 'orange'
            status = 'Concept'
        else:
            color = 'blue'
            status = 'In Development'

        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            status
        )

    status_badge.short_description = 'Status'  # type: ignore

    def crew_range(self, obj: Ship) -> str:
        """Display crew requirements range.

        Args:
            obj: Ship instance

        Returns:
            str: Crew range string
        """
        if obj.crew_min and obj.crew_max:
            return f"{obj.crew_min}-{obj.crew_max}"
        elif obj.crew_min:
            return f"{obj.crew_min}+"
        elif obj.crew_max:
            return f"Up to {obj.crew_max}"
        return '-'

    crew_range.short_description = 'Crew'  # type: ignore

    @admin.action(description='Mark selected ships as flight ready')
    def mark_flight_ready(self, request: Any, queryset: Any) -> None:
        """Bulk action to mark ships as flight ready.

        Args:
            request: HTTP request object
            queryset: Selected ships queryset
        """
        updated = queryset.update(is_flight_ready=True, is_concept=False)
        self.message_user(request, f'{updated} ships marked as flight ready.')

    @admin.action(description='Mark selected ships as concept')
    def mark_concept(self, request: Any, queryset: Any) -> None:
        """Bulk action to mark ships as concept.

        Args:
            request: HTTP request object
            queryset: Selected ships queryset
        """
        updated = queryset.update(is_concept=True, is_flight_ready=False)
        self.message_user(request, f'{updated} ships marked as concept.')


@admin.register(ShipComponent)
class ShipComponentAdmin(admin.ModelAdmin):
    """Admin interface for ship components."""

    list_display = ('name', 'ship', 'type', 'size', 'quantity')
    list_filter = ('type', 'ship__manufacturer')
    search_fields = ('name', 'ship__name')
    ordering = ('ship', 'type', 'name')

    fieldsets = (
        ('Component Information', {
            'fields': ('ship', 'type', 'name', 'size', 'quantity')
        }),
    )
