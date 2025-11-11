"""Fleet admin interface."""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import FleetShip


@admin.register(FleetShip)
class FleetShipAdmin(admin.ModelAdmin):
    list_display = [
        'ship_display',
        'owner',
        'custom_name',
        'status',
        'is_available_for_missions',
        'purchased_date'
    ]
    list_filter = ['status', 'is_available_for_missions', 'ship__type', 'ship__manufacturer']
    search_fields = ['name', 'ship__name', 'owner__username', 'notes']
    autocomplete_fields = ['ship', 'owner']
    date_hierarchy = 'purchased_date'

    fieldsets = (
        (_('Ship Details'), {
            'fields': ('ship', 'owner', 'name')
        }),
        (_('Status'), {
            'fields': ('status', 'purchased_date', 'is_available_for_missions')
        }),
        (_('Additional Info'), {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )

    def ship_display(self, obj):
        return f"{obj.ship.manufacturer.name} {obj.ship.name}"
    ship_display.short_description = _('Ship')
    ship_display.admin_order_field = 'ship__name'

    def custom_name(self, obj):
        return obj.name if obj.name else '-'
    custom_name.short_description = _('Custom Name')
