"""
Squadron models for organizing members into specialized groups.
"""
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify


class Squadron(models.Model):
    """Squadron/Division within the organization."""

    # Basic info
    name = models.CharField(_('Squadron Name'), max_length=100, unique=True)
    slug = models.SlugField(_('Slug'), max_length=100, unique=True, blank=True)
    callsign = models.CharField(_('Callsign'), max_length=50, unique=True, help_text='Squadron callsign/code (e.g., ALPHA, BRAVO)')

    # Description
    description = models.TextField(_('Description'), blank=True)
    motto = models.CharField(_('Motto'), max_length=200, blank=True)

    # Leadership
    commander = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='commanded_squadrons',
        verbose_name=_('Commander')
    )

    # Squadron focus/specialization
    FOCUS_CHOICES = [
        ('combat', 'Combat Operations'),
        ('exploration', 'Exploration'),
        ('trading', 'Trading & Commerce'),
        ('mining', 'Mining Operations'),
        ('security', 'Security & Escort'),
        ('support', 'Support & Logistics'),
        ('mixed', 'Mixed Operations'),
    ]
    focus = models.CharField(
        _('Focus'),
        max_length=50,
        choices=FOCUS_CHOICES,
        default='mixed'
    )

    # Status
    is_active = models.BooleanField(_('Active'), default=True, db_index=True)
    is_recruiting = models.BooleanField(_('Recruiting'), default=False)

    # Limits
    max_members = models.IntegerField(
        _('Max Members'),
        null=True,
        blank=True,
        help_text='Maximum number of members (leave blank for unlimited)'
    )

    # Metadata
    logo_url = models.URLField(_('Logo URL'), blank=True)
    color_code = models.CharField(
        _('Color Code'),
        max_length=7,
        default='#55E6A5',
        help_text='Hex color code for squadron (e.g., #55E6A5)'
    )

    # Timestamps
    created_at = models.DateTimeField(_('Created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated'), auto_now=True)

    class Meta:
        db_table = 'squadrons'
        verbose_name = _('Squadron')
        verbose_name_plural = _('Squadrons')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.callsign})"

    def save(self, *args, **kwargs):
        """Generate slug from name if not provided."""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_member_count(self):
        """Get current member count."""
        return self.members.count()

    def is_full(self):
        """Check if squadron is at capacity."""
        if self.max_members is None:
            return False
        return self.get_member_count() >= self.max_members

    def can_accept_members(self):
        """Check if squadron can accept new members."""
        return self.is_active and self.is_recruiting and not self.is_full()


class SquadronMember(models.Model):
    """Member assignment to squadron with role."""

    # Relationships
    squadron = models.ForeignKey(
        Squadron,
        on_delete=models.CASCADE,
        related_name='members',
        verbose_name=_('Squadron')
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='squadron_memberships',
        verbose_name=_('User')
    )

    # Role in squadron
    ROLE_CHOICES = [
        ('member', 'Member'),
        ('lead', 'Squad Lead'),
        ('officer', 'Officer'),
        ('specialist', 'Specialist'),
    ]
    role = models.CharField(
        _('Role'),
        max_length=50,
        choices=ROLE_CHOICES,
        default='member'
    )

    # Status
    is_active = models.BooleanField(_('Active'), default=True, db_index=True)

    # Dates
    joined_at = models.DateTimeField(_('Joined'), auto_now_add=True)
    left_at = models.DateTimeField(_('Left'), null=True, blank=True)

    # Notes
    notes = models.TextField(_('Notes'), blank=True)

    class Meta:
        db_table = 'squadron_members'
        verbose_name = _('Squadron Member')
        verbose_name_plural = _('Squadron Members')
        ordering = ['squadron', '-joined_at']
        unique_together = [['squadron', 'user']]
        indexes = [
            models.Index(fields=['squadron', 'is_active']),
            models.Index(fields=['user', 'is_active']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.squadron.name} ({self.get_role_display()})"

    def leave_squadron(self):
        """Mark member as having left the squadron."""
        from django.utils import timezone
        self.is_active = False
        self.left_at = timezone.now()
        self.save(update_fields=['is_active', 'left_at'])
