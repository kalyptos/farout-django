"""Admin interface for squadron app."""
from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import Squadron, SquadronMember


class SquadronMemberInline(admin.TabularInline):
    """Inline admin for squadron members."""
    model = SquadronMember
    extra = 0
    fields = ('user', 'role', 'is_active', 'joined_at')
    readonly_fields = ('joined_at',)
    autocomplete_fields = ['user']


@admin.register(Squadron)
class SquadronAdmin(admin.ModelAdmin):
    """Admin for squadrons."""

    list_display = (
        'name',
        'callsign',
        'focus',
        'commander',
        'member_count',
        'status_badges',
        'created_at',
    )
    list_filter = ('focus', 'is_active', 'is_recruiting', 'created_at')
    search_fields = ('name', 'callsign', 'description', 'motto')
    prepopulated_fields = {'slug': ('name',)}
    autocomplete_fields = ['commander']
    readonly_fields = ('created_at', 'updated_at', 'member_count')

    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name', 'slug', 'callsign', 'description', 'motto')
        }),
        (_('Leadership & Focus'), {
            'fields': ('commander', 'focus')
        }),
        (_('Settings'), {
            'fields': ('is_active', 'is_recruiting', 'max_members')
        }),
        (_('Appearance'), {
            'fields': ('logo_url', 'color_code')
        }),
        (_('Statistics'), {
            'fields': ('member_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    inlines = [SquadronMemberInline]

    def member_count(self, obj):
        """Display member count."""
        count = obj.get_member_count()
        if obj.max_members:
            return f"{count}/{obj.max_members}"
        return str(count)
    member_count.short_description = _('Members')

    def status_badges(self, obj):
        """Display status badges."""
        badges = []
        if obj.is_active:
            badges.append('<span style="background-color: #45b7d1; color: white; padding: 2px 8px; border-radius: 3px; font-size: 10px;">ACTIVE</span>')
        if obj.is_recruiting:
            badges.append('<span style="background-color: #55E6A5; color: #1a1a2e; padding: 2px 8px; border-radius: 3px; font-size: 10px;">RECRUITING</span>')
        if obj.is_full():
            badges.append('<span style="background-color: #ff6b6b; color: white; padding: 2px 8px; border-radius: 3px; font-size: 10px;">FULL</span>')
        return format_html(' '.join(badges)) if badges else '-'
    status_badges.short_description = _('Status')


@admin.register(SquadronMember)
class SquadronMemberAdmin(admin.ModelAdmin):
    """Admin for squadron members."""

    list_display = (
        'user',
        'squadron',
        'role',
        'is_active',
        'joined_at',
    )
    list_filter = ('squadron', 'role', 'is_active', 'joined_at')
    search_fields = ('user__username', 'user__email', 'squadron__name')
    autocomplete_fields = ['user', 'squadron']
    readonly_fields = ('joined_at', 'left_at')
    date_hierarchy = 'joined_at'

    fieldsets = (
        (_('Assignment'), {
            'fields': ('squadron', 'user', 'role')
        }),
        (_('Status'), {
            'fields': ('is_active', 'joined_at', 'left_at')
        }),
        (_('Notes'), {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )

    actions = ['activate_members', 'deactivate_members']

    def activate_members(self, request, queryset):
        """Activate selected members."""
        updated = queryset.update(is_active=True, left_at=None)
        self.message_user(request, _(f'{updated} members activated.'))
    activate_members.short_description = _('Activate members')

    def deactivate_members(self, request, queryset):
        """Deactivate selected members."""
        from django.utils import timezone
        updated = queryset.update(is_active=False, left_at=timezone.now())
        self.message_user(request, _(f'{updated} members deactivated.'))
    deactivate_members.short_description = _('Deactivate members')
