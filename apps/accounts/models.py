"""
Custom User model with Discord OAuth fields.
Extends AbstractUser to include Discord-specific fields and role management.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    """
    Custom User model for Farout organization portal.
    Includes Discord OAuth integration and role-based access control.
    """

    # Role choices
    ROLE_MEMBER = 'member'
    ROLE_ADMIN = 'admin'

    ROLE_CHOICES = [
        (ROLE_MEMBER, 'Member'),
        (ROLE_ADMIN, 'Admin'),
    ]

    # Discord OAuth fields
    discord_id = models.CharField(
        max_length=100,
        unique=True,
        null=True,
        blank=True,
        db_index=True,
        help_text='Discord user ID'
    )

    discriminator = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        help_text='Discord discriminator (deprecated by Discord)'
    )

    avatar = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text='Discord avatar hash'
    )

    # Profile picture upload
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        null=True,
        blank=True,
        help_text='Uploaded profile picture (overrides Discord avatar)'
    )

    # Additional fields
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_MEMBER,
        db_index=True,
        help_text='User role in the organization'
    )

    rank_image = models.URLField(
        max_length=500,
        null=True,
        blank=True,
        help_text='URL to rank image'
    )

    must_change_password = models.BooleanField(
        default=False,
        help_text='Force password change on next login'
    )

    last_login_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Last login timestamp'
    )

    # Override email to make it optional
    email = models.EmailField(
        'email address',
        blank=True,
        null=True,
        unique=False  # Discord users may not have unique emails
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['discord_id']),
            models.Index(fields=['role']),
            models.Index(fields=['username']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        """Check if user has admin role."""
        return self.role == self.ROLE_ADMIN

    @property
    def discord_avatar_url(self):
        """Generate full Discord avatar URL."""
        if self.discord_id and self.avatar:
            return f"https://cdn.discordapp.com/avatars/{self.discord_id}/{self.avatar}.png"
        return None

    def get_avatar_url(self):
        """Get avatar URL with priority: uploaded > Discord > default."""
        # Priority 1: Uploaded profile picture
        if self.profile_picture:
            return self.profile_picture.url

        # Priority 2: Discord avatar
        discord_url = self.discord_avatar_url
        if discord_url:
            return discord_url

        # Priority 3: Default avatar
        return '/static/img/default-avatar.svg'

    def update_last_login(self):
        """Update last login timestamp."""
        self.last_login_at = timezone.now()
        self.save(update_fields=['last_login_at'])
