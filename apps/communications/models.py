"""
Communications models for contact forms and internal messaging.

These models use the 'communications' database for isolation and scaling.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _


class ContactSubmission(models.Model):
    """Contact form submissions from public users."""

    # Contact info
    name = models.CharField(_('Name'), max_length=200)
    email = models.EmailField(_('Email'))
    subject = models.CharField(_('Subject'), max_length=300)
    message = models.TextField(_('Message'))

    # Metadata
    ip_address = models.GenericIPAddressField(_('IP Address'), null=True, blank=True)
    user_agent = models.TextField(_('User Agent'), blank=True)

    # Status
    STATUS_CHOICES = [
        ('new', 'New'),
        ('read', 'Read'),
        ('replied', 'Replied'),
        ('archived', 'Archived'),
    ]
    status = models.CharField(
        _('Status'),
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        db_index=True
    )

    # Response
    response_sent = models.BooleanField(_('Response Sent'), default=False)
    response_sent_at = models.DateTimeField(_('Response Sent At'), null=True, blank=True)

    # Spam protection
    is_spam = models.BooleanField(_('Marked as Spam'), default=False, db_index=True)

    # Timestamps
    created_at = models.DateTimeField(_('Created'), auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(_('Updated'), auto_now=True)

    class Meta:
        db_table = 'contact_submissions'
        verbose_name = _('Contact Submission')
        verbose_name_plural = _('Contact Submissions')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at', 'status']),
            models.Index(fields=['email']),
        ]

    def __str__(self):
        return f"{self.name} - {self.subject} ({self.get_status_display()})"


class InternalMessage(models.Model):
    """Internal messages between organization members."""

    # Sender/Receiver (using user_id as integer to avoid FK to main database)
    sender_id = models.IntegerField(_('Sender User ID'), db_index=True)
    sender_name = models.CharField(_('Sender Name'), max_length=200)

    recipient_id = models.IntegerField(_('Recipient User ID'), db_index=True)
    recipient_name = models.CharField(_('Recipient Name'), max_length=200)

    # Message content
    subject = models.CharField(_('Subject'), max_length=300)
    message = models.TextField(_('Message'))

    # Thread tracking
    parent_message_id = models.IntegerField(
        _('Parent Message ID'),
        null=True,
        blank=True,
        help_text='ID of parent message for threading'
    )

    # Status
    is_read = models.BooleanField(_('Read'), default=False, db_index=True)
    read_at = models.DateTimeField(_('Read At'), null=True, blank=True)

    is_deleted_by_sender = models.BooleanField(_('Deleted by Sender'), default=False)
    is_deleted_by_recipient = models.BooleanField(_('Deleted by Recipient'), default=False)

    # System messages (announcements from admins)
    is_system_message = models.BooleanField(_('System Message'), default=False, db_index=True)
    is_announcement = models.BooleanField(_('Announcement'), default=False)

    # Timestamps
    created_at = models.DateTimeField(_('Sent'), auto_now_add=True, db_index=True)

    class Meta:
        db_table = 'internal_messages'
        verbose_name = _('Internal Message')
        verbose_name_plural = _('Internal Messages')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient_id', '-created_at']),
            models.Index(fields=['sender_id', '-created_at']),
            models.Index(fields=['recipient_id', 'is_read']),
        ]

    def __str__(self):
        return f"{self.sender_name} → {self.recipient_name}: {self.subject}"

    def mark_as_read(self):
        """Mark message as read."""
        if not self.is_read:
            from django.utils import timezone
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at'])
