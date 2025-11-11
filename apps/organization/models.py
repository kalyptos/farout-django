"""
Organization models for managing Star Citizen organizations and members.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _


class Organization(models.Model):
    """Star Citizen Organizations."""

    # Basic info
    sid = models.CharField(
        _('SID'),
        max_length=10,
        unique=True,
        help_text=_('Organization SID (e.g., FAROUT)')
    )
    name = models.CharField(_('Name'), max_length=200)
    url = models.URLField(_('URL'), blank=True)

    # Details
    archetype = models.CharField(_('Archetype'), max_length=100, blank=True)
    commitment = models.CharField(_('Commitment'), max_length=100, blank=True)
    primary_language = models.CharField(_('Primary Language'), max_length=50, blank=True)
    recruiting = models.BooleanField(_('Recruiting'), default=False)

    # Stats
    member_count = models.IntegerField(_('Member Count'), default=0)

    # Description
    headline = models.TextField(_('Headline'), blank=True)
    description = models.TextField(_('Description'), blank=True)
    history = models.TextField(_('History'), blank=True)
    manifesto = models.TextField(_('Manifesto'), blank=True)
    charter = models.TextField(_('Charter'), blank=True)

    # Media
    logo_url = models.URLField(_('Logo URL'), blank=True)
    banner_url = models.URLField(_('Banner URL'), blank=True)

    # API metadata
    api_data = models.JSONField(_('API Data'), default=dict, blank=True)

    # Timestamps
    created_at = models.DateTimeField(_('Created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated'), auto_now=True)

    class Meta:
        verbose_name = _('Organization')
        verbose_name_plural = _('Organizations')
        ordering = ['name']

    def __str__(self) -> str:
        return f"{self.name} ({self.sid})"


class OrganizationMember(models.Model):
    """Members of Star Citizen organizations."""

    # Basic info
    handle = models.CharField(
        _('Handle'),
        max_length=100,
        unique=True,
        help_text=_('Star Citizen handle')
    )
    display_name = models.CharField(_('Display Name'), max_length=200)

    # Org details
    rank = models.CharField(_('Rank'), max_length=100, blank=True)
    stars = models.IntegerField(_('Stars'), default=0)

    # Profile
    avatar_url = models.URLField(_('Avatar URL'), blank=True)
    bio = models.TextField(_('Bio'), blank=True)

    # API metadata
    api_data = models.JSONField(_('API Data'), default=dict, blank=True)

    # Timestamps
    created_at = models.DateTimeField(_('Created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated'), auto_now=True)

    class Meta:
        verbose_name = _('Organization Member')
        verbose_name_plural = _('Organization Members')
        ordering = ['-stars', 'handle']
        indexes = [
            models.Index(fields=['handle']),
            models.Index(fields=['-stars']),
        ]

    def __str__(self) -> str:
        return f"{self.display_name} ({self.handle})"
