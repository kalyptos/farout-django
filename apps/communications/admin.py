"""Admin interface for communications app."""
from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import ContactSubmission, InternalMessage


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    """Admin for contact form submissions."""

    list_display = (
        'name',
        'email',
        'subject',
        'status_badge',
        'created_at',
        'is_spam',
    )
    list_filter = ('status', 'is_spam', 'response_sent', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at', 'updated_at', 'ip_address', 'user_agent')
    date_hierarchy = 'created_at'

    fieldsets = (
        (_('Contact Information'), {
            'fields': ('name', 'email', 'subject', 'message')
        }),
        (_('Status'), {
            'fields': ('status', 'is_spam', 'response_sent', 'response_sent_at')
        }),
        (_('Metadata'), {
            'fields': ('ip_address', 'user_agent', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['mark_as_read', 'mark_as_spam', 'mark_as_not_spam', 'archive']

    def status_badge(self, obj):
        """Display status with color badge."""
        colors = {
            'new': '#ff6b6b',
            'read': '#4ecdc4',
            'replied': '#45b7d1',
            'archived': '#95a5a6',
        }
        color = colors.get(obj.status, '#95a5a6')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; font-size: 11px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = _('Status')

    def mark_as_read(self, request, queryset):
        """Mark selected submissions as read."""
        updated = queryset.update(status='read')
        self.message_user(request, _(f'{updated} submissions marked as read.'))
    mark_as_read.short_description = _('Mark as read')

    def mark_as_spam(self, request, queryset):
        """Mark selected submissions as spam."""
        updated = queryset.update(is_spam=True, status='archived')
        self.message_user(request, _(f'{updated} submissions marked as spam.'))
    mark_as_spam.short_description = _('Mark as spam')

    def mark_as_not_spam(self, request, queryset):
        """Mark selected submissions as not spam."""
        updated = queryset.update(is_spam=False)
        self.message_user(request, _(f'{updated} submissions marked as not spam.'))
    mark_as_not_spam.short_description = _('Mark as not spam')

    def archive(self, request, queryset):
        """Archive selected submissions."""
        updated = queryset.update(status='archived')
        self.message_user(request, _(f'{updated} submissions archived.'))
    archive.short_description = _('Archive')


@admin.register(InternalMessage)
class InternalMessageAdmin(admin.ModelAdmin):
    """Admin for internal messages."""

    list_display = (
        'sender_name',
        'recipient_name',
        'subject',
        'is_read',
        'is_system_message',
        'created_at',
    )
    list_filter = ('is_read', 'is_system_message', 'is_announcement', 'created_at')
    search_fields = ('sender_name', 'recipient_name', 'subject', 'message')
    readonly_fields = ('created_at', 'read_at')
    date_hierarchy = 'created_at'

    fieldsets = (
        (_('From/To'), {
            'fields': (
                ('sender_id', 'sender_name'),
                ('recipient_id', 'recipient_name'),
            )
        }),
        (_('Message'), {
            'fields': ('subject', 'message', 'parent_message_id')
        }),
        (_('Status'), {
            'fields': (
                'is_read',
                'read_at',
                'is_system_message',
                'is_announcement',
                'is_deleted_by_sender',
                'is_deleted_by_recipient',
            )
        }),
        (_('Timestamps'), {
            'fields': ('created_at',)
        }),
    )

    actions = ['mark_as_read', 'mark_as_unread']

    def mark_as_read(self, request, queryset):
        """Mark selected messages as read."""
        from django.utils import timezone
        updated = queryset.update(is_read=True, read_at=timezone.now())
        self.message_user(request, _(f'{updated} messages marked as read.'))
    mark_as_read.short_description = _('Mark as read')

    def mark_as_unread(self, request, queryset):
        """Mark selected messages as unread."""
        updated = queryset.update(is_read=False, read_at=None)
        self.message_user(request, _(f'{updated} messages marked as unread.'))
    mark_as_unread.short_description = _('Mark as unread')
