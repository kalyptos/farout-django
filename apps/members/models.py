"""
Member model for organization members.
Stores Star Citizen organization member information.
"""
from __future__ import annotations
from django.db import models
from typing import Any, Dict, List


class Member(models.Model):
    """
    Organization member with Star Citizen specific fields.
    """

    # Rank choices (Star Citizen typical ranks)
    RANK_CHOICES = [
        ('recruit', 'Recruit'),
        ('member', 'Member'),
        ('veteran', 'Veteran'),
        ('officer', 'Officer'),
        ('leader', 'Leader'),
    ]

    discord_id = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        help_text='Discord user ID'
    )

    display_name = models.CharField(
        max_length=255,
        help_text='Display name in organization'
    )

    bio = models.TextField(
        blank=True,
        null=True,
        help_text='Member biography'
    )

    avatar_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text='Avatar image URL'
    )

    rank = models.CharField(
        max_length=50,
        choices=RANK_CHOICES,
        default='member',
        db_index=True,
        help_text='Member rank in organization'
    )

    # Use callable defaults to avoid mutable default issues
    missions_completed = models.JSONField(
        default=list,  # Django's JSONField handles this correctly, but explicit is better
        blank=True,
        help_text='List of completed mission objects with details'
    )

    trainings_completed = models.JSONField(
        default=list,  # Django's JSONField handles this correctly
        blank=True,
        help_text='List of completed training objects with details'
    )

    stats = models.JSONField(
        default=dict,  # Django's JSONField handles this correctly
        blank=True,
        help_text='Member statistics dictionary (kills, deaths, playtime, etc.)'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'members'
        verbose_name = 'Member'
        verbose_name_plural = 'Members'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['discord_id']),
            models.Index(fields=['rank']),
            models.Index(fields=['display_name']),
        ]

    def __str__(self) -> str:
        """Return string representation of member.

        Returns:
            str: Display name and rank of the member
        """
        return f"{self.display_name} ({self.rank})"

    @property
    def total_missions(self) -> int:
        """Get total number of completed missions.

        Returns:
            int: Count of completed missions
        """
        return len(self.missions_completed) if isinstance(self.missions_completed, list) else 0

    @property
    def total_trainings(self) -> int:
        """Get total number of completed trainings.

        Returns:
            int: Count of completed trainings
        """
        return len(self.trainings_completed) if isinstance(self.trainings_completed, list) else 0
