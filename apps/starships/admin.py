"""Starships admin interface."""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Manufacturer, Ship, ShipComponent


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'created_at']
    search_fields = ['code', 'name']
    list_filter = ['created_at']
    ordering = ['name']


class ShipComponentInline(admin.TabularInline):
    model = ShipComponent
    extra = 0
    fields = ['component_type', 'name', 'size', 'quantity']


@admin.register(Ship)
class ShipAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'manufacturer',
        'type',
        'size',
        'is_flight_ready',
        'is_concept',
        'cargo_capacity',
        'min_crew',
        'pledge_price'
    ]
    list_filter = [
        'manufacturer',
        'type',
        'size',
        'is_flight_ready',
        'is_concept',
        'production_status'
    ]
    search_fields = ['name', 'manufacturer__name', 'description', 'type']
    autocomplete_fields = ['manufacturer']
    readonly_fields = ['created_at', 'updated_at', 'api_data']
    inlines = [ShipComponentInline]

    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name', 'manufacturer', 'type', 'size', 'focus')
        }),
        (_('Description'), {
            'fields': ('description', 'career', 'role')
        }),
        (_('Technical Specifications'), {
            'fields': (
                ('length', 'beam', 'height'),
                'mass',
                ('min_crew', 'max_crew'),
                'cargo_capacity'
            ),
            'classes': ('collapse',)
        }),
        (_('Status & Pricing'), {
            'fields': (
                'is_flight_ready',
                'is_concept',
                'production_status',
                'pledge_price'
            )
        }),
        (_('Media'), {
            'fields': ('image_url', 'store_url'),
            'classes': ('collapse',)
        }),
        (_('API Data'), {
            'fields': ('api_id', 'api_data', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ShipComponent)
class ShipComponentAdmin(admin.ModelAdmin):
    list_display = ['ship', 'component_type', 'name', 'size', 'quantity']
    list_filter = ['component_type', 'size']
    search_fields = ['ship__name', 'name', 'mount_name']
    autocomplete_fields = ['ship']
