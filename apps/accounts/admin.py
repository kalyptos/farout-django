"""
Admin configuration for User model.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom admin for User model with Discord OAuth fields.
    """

    list_display = ('username', 'email', 'role', 'discord_id', 'is_active', 'is_staff', 'created_at')
    list_filter = ('role', 'is_active', 'is_staff', 'is_superuser', 'created_at')
    search_fields = ('username', 'email', 'discord_id')
    ordering = ('-created_at',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Discord OAuth', {'fields': ('discord_id', 'avatar', 'discriminator')}),
        ('Organization', {'fields': ('role', 'rank_image')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'last_login_at', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'role', 'is_staff', 'is_active'),
        }),
    )

    readonly_fields = ('last_login', 'date_joined', 'created_at', 'updated_at')

    actions = ['make_admin', 'make_member']

    def make_admin(self, request, queryset):
        """Bulk action to promote users to admin."""
        queryset.update(role=User.ROLE_ADMIN)
        self.message_user(request, f'{queryset.count()} user(s) promoted to admin.')
    make_admin.short_description = 'Promote selected users to Admin'

    def make_member(self, request, queryset):
        """Bulk action to demote users to member."""
        queryset.update(role=User.ROLE_MEMBER)
        self.message_user(request, f'{queryset.count()} user(s) demoted to member.')
    make_member.short_description = 'Demote selected users to Member'
