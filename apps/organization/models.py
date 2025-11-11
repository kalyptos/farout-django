"""
Models for Star Citizen organizations and members.
"""
from __future__ import annotations
from django.db import models
from django.conf import settings
from typing import Optional


class Organization(models.Model):
    """
    Star Citizen organization information.
    Synced from Star Citizen API.
    """

    sid = models.CharField(
        max_length=20,
        unique=True,
        db_index=True,
        help_text='Organization SID (e.g., FAROUT, TEST)'
    )

    name = models.CharField(
        max_length=200,
        help_text='Organization full name'
    )

    archetype = models.CharField(
        max_length=50,
        blank=True,
        help_text='Organization archetype (PMC, Trading, etc.)'
    )

    commitment = models.CharField(
        max_length=50,
        blank=True,
        help_text='Commitment level (Casual, Regular, Hardcore)'
    )

    description = models.TextField(
        blank=True,
        help_text='Organization description and charter'
    )

    # Statistics
    member_count = models.PositiveIntegerField(
        default=0,
        help_text='Total number of members'
    )

    # Media
    banner_url = models.URLField(
        max_length=500,
        blank=True,
        help_text='Organization banner image URL'
    )

    logo_url = models.URLField(
        max_length=500,
        blank=True,
        help_text='Organization logo URL'
    )

    url = models.URLField(
        max_length=500,
        blank=True,
        help_text='Organization website or RSI page'
    )

    # API metadata
    api_data = models.JSONField(
        default=dict,
        blank=True,
        help_text='Full API response data'
    )

    last_synced = models.DateTimeField(
        auto_now=True,
        help_text='Last sync from Star Citizen API'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'organizations'
        verbose_name = 'Organization'
        verbose_name_plural = 'Organizations'
        ordering = ['name']
        indexes = [
            models.Index(fields=['sid']),
            models.Index(fields=['name']),
        ]

    def __str__(self) -> str:
        """Return string representation of organization.

        Returns:
            str: Organization name and SID
        """
        return f"{self.name} ({self.sid})"

    @property
    def rsi_url(self) -> str:
        """Generate RSI organization page URL.

        Returns:
            str: Full RSI URL
        """
        return f"https://robertsspaceindustries.com/orgs/{self.sid}"


class OrganizationMember(models.Model):
    """
    Star Citizen organization member.
    Links SC handles to our User accounts.
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='members',
        help_text='Organization this member belongs to'
    )

    handle = models.CharField(
        max_length=100,
        db_index=True,
        help_text='Star Citizen handle/username'
    )

    display_name = models.CharField(
        max_length=200,
        blank=True,
        help_text='Display name (may differ from handle)'
    )

    # Link to local user account
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sc_member',
        help_text='Linked user account (if authenticated via Discord)'
    )

    # Organization-specific info
    rank = models.CharField(
        max_length=100,
        blank=True,
        help_text='Rank within organization'
    )

    stars = models.PositiveIntegerField(
        default=0,
        help_text='Star rank (0-5)'
    )

    # Media
    avatar_url = models.URLField(
        max_length=500,
        blank=True,
        help_text='Member avatar URL from RSI'
    )

    # API metadata
    api_data = models.JSONField(
        default=dict,
        blank=True,
        help_text='Full API response data'
    )

    last_synced = models.DateTimeField(
        auto_now=True,
        help_text='Last sync from Star Citizen API'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'organization_members'
        verbose_name = 'Organization Member'
        verbose_name_plural = 'Organization Members'
        ordering = ['-stars', 'handle']
        unique_together = [['organization', 'handle']]
        indexes = [
            models.Index(fields=['organization', 'handle']),
            models.Index(fields=['handle']),
            models.Index(fields=['-stars']),
        ]

    def __str__(self) -> str:
        """Return string representation of member.

        Returns:
            str: Member handle with organization
        """
        return f"{self.handle} ({self.organization.sid})"

    @property
    def citizen_url(self) -> str:
        """Generate RSI citizen profile URL.

        Returns:
            str: Full RSI URL
        """
        return f"https://robertsspaceindustries.com/citizens/{self.handle}"

    @property
    def is_linked(self) -> bool:
        """Check if member is linked to a user account.

        Returns:
            bool: True if linked to user account
        """
        return self.user is not None
