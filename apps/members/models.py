"""
Member model for organization members.
Stores Star Citizen organization member information.
"""
from django.db import models


class Member(models.Model):
    """
    Organization member with Star Citizen specific fields.
    """

    # Rank choices (Star Citizen typical ranks)
    RANK_CHOICES = [
        ('private', 'Private'),
        ('corporal', 'Corporal'),
        ('sergeant', 'Sergeant'),
        ('lieutenant', 'Lieutenant'),
        ('captain', 'Captain'),
        ('major', 'Major'),
        ('colonel', 'Colonel'),
        ('commander', 'Commander'),
        ('admiral', 'Admiral'),
        ('fleet_admiral', 'Fleet Admiral'),
    ]

    # Role choices
    ROLE_CHOICES = [
        ('user', 'User'),
        ('member', 'Member'),
        ('admin', 'Admin'),
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

    profile_image = models.ImageField(
        upload_to='member_profiles/',
        blank=True,
        null=True,
        help_text='Star Citizen character profile image'
    )

    rank = models.CharField(
        max_length=50,
        choices=RANK_CHOICES,
        default='private',
        db_index=True,
        help_text='Member rank in organization'
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='user',
        db_index=True,
        help_text='Member role in organization'
    )

    squadron = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text='Squadron assignment'
    )

    missions_completed = models.JSONField(
        default=list,
        blank=True,
        help_text='List of completed missions'
    )

    trainings_completed = models.JSONField(
        default=list,
        blank=True,
        help_text='List of completed trainings'
    )

    stats = models.JSONField(
        default=dict,
        blank=True,
        help_text='Member statistics (kills, deaths, etc.)'
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

    def __str__(self):
        return f"{self.display_name} ({self.rank})"

    @property
    def total_missions(self):
        """Get total number of completed missions."""
        return len(self.missions_completed)

    @property
    def total_trainings(self):
        """Get total number of completed trainings."""
        return len(self.trainings_completed)

    def get_rank_image_url(self):
        """Get rank badge image URL based on rank."""
        rank_images = {
            'private': 'https://starcitizen.tools/images/thumb/9/9e/Rank_1.svg/100px-Rank_1.svg.png',
            'corporal': 'https://starcitizen.tools/images/thumb/b/b2/Rank_2.svg/100px-Rank_2.svg.png',
            'sergeant': 'https://starcitizen.tools/images/thumb/3/3c/Rank_3.svg/100px-Rank_3.svg.png',
            'lieutenant': 'https://starcitizen.tools/images/thumb/0/0e/Rank_4.svg/100px-Rank_4.svg.png',
            'captain': 'https://starcitizen.tools/images/thumb/f/f3/Rank_5.svg/100px-Rank_5.svg.png',
            'major': 'https://starcitizen.tools/images/thumb/7/75/Rank_6.svg/100px-Rank_6.svg.png',
            'colonel': 'https://starcitizen.tools/images/thumb/1/1c/Rank_7.svg/100px-Rank_7.svg.png',
            'commander': 'https://starcitizen.tools/images/thumb/8/8f/Rank_8.svg/100px-Rank_8.svg.png',
            'admiral': 'https://starcitizen.tools/images/thumb/a/a7/Rank_9.svg/100px-Rank_9.svg.png',
            'fleet_admiral': 'https://starcitizen.tools/images/thumb/5/5e/Rank_10.svg/100px-Rank_10.svg.png',
        }
        return rank_images.get(self.rank, rank_images['private'])

    def get_profile_image_url(self):
        """Get profile image URL (prioritize uploaded image, fallback to avatar)."""
        if self.profile_image:
            return self.profile_image.url
        return self.avatar_url


class ShipOwnership(models.Model):
    """
    Track ship ownership by members.
    """
    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name='ship_ownerships',
        help_text='Member who owns the ship'
    )

    ship = models.ForeignKey(
        'starships.Ship',
        on_delete=models.CASCADE,
        related_name='ownerships',
        help_text='Ship owned'
    )

    quantity = models.PositiveIntegerField(
        default=1,
        help_text='Number of ships owned'
    )

    acquired_date = models.DateTimeField(
        auto_now_add=True,
        help_text='Date acquired'
    )

    notes = models.TextField(
        blank=True,
        null=True,
        help_text='Additional notes'
    )

    class Meta:
        db_table = 'ship_ownerships'
        verbose_name = 'Ship Ownership'
        verbose_name_plural = 'Ship Ownerships'
        unique_together = ['member', 'ship']
        ordering = ['-acquired_date']

    def __str__(self):
        return f"{self.member.display_name} owns {self.quantity}x {self.ship.name}"
