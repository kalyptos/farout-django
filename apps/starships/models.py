"""
Models for Star Citizen ships and manufacturers.
"""
from __future__ import annotations
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from typing import Any


class Manufacturer(models.Model):
    """
    Star Citizen ship manufacturers (e.g., Aegis Dynamics, Origin Jumpworks, RSI).
    """

    name = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        help_text='Manufacturer name (e.g., Aegis Dynamics)'
    )

    code = models.CharField(
        max_length=10,
        unique=True,
        db_index=True,
        help_text='Manufacturer code/abbreviation (e.g., AEGS, ORIG, RSI)'
    )

    description = models.TextField(
        blank=True,
        help_text='Manufacturer description and history'
    )

    logo_url = models.URLField(
        max_length=500,
        blank=True,
        help_text='URL to manufacturer logo image'
    )

    # API metadata
    api_data = models.JSONField(
        default=dict,
        blank=True,
        help_text='Full API response data for reference'
    )

    last_updated = models.DateTimeField(
        auto_now=True,
        help_text='Last sync from Star Citizen API'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ship_manufacturers'
        verbose_name = 'Ship Manufacturer'
        verbose_name_plural = 'Ship Manufacturers'
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['code']),
        ]

    def __str__(self) -> str:
        """Return string representation of manufacturer.

        Returns:
            str: Manufacturer name
        """
        return self.name


class Ship(models.Model):
    """
    Star Citizen ships and vehicles with specifications.
    """

    # Ship size choices
    SIZE_VEHICLE = 'vehicle'
    SIZE_SNUB = 'snub'
    SIZE_SMALL = 'small'
    SIZE_MEDIUM = 'medium'
    SIZE_LARGE = 'large'
    SIZE_CAPITAL = 'capital'

    SIZE_CHOICES = [
        (SIZE_VEHICLE, 'Vehicle'),
        (SIZE_SNUB, 'Snub Fighter'),
        (SIZE_SMALL, 'Small'),
        (SIZE_MEDIUM, 'Medium'),
        (SIZE_LARGE, 'Large'),
        (SIZE_CAPITAL, 'Capital'),
    ]

    # Basic information
    name = models.CharField(
        max_length=200,
        db_index=True,
        help_text='Ship name (e.g., Sabre, Constellation Andromeda)'
    )

    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.PROTECT,  # Don't delete manufacturer if ships exist
        related_name='ships',
        help_text='Ship manufacturer'
    )

    # Ship details
    model = models.CharField(
        max_length=100,
        help_text='Ship model designation'
    )

    type = models.CharField(
        max_length=50,
        blank=True,
        db_index=True,
        help_text='Ship type/role (Fighter, Transport, Mining, etc.)'
    )

    size = models.CharField(
        max_length=20,
        choices=SIZE_CHOICES,
        blank=True,
        db_index=True,
        help_text='Ship size classification'
    )

    focus = models.CharField(
        max_length=100,
        blank=True,
        help_text='Primary focus/specialty'
    )

    description = models.TextField(
        blank=True,
        help_text='Ship description and lore'
    )

    # Physical specifications (in meters)
    length = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text='Ship length in meters'
    )

    beam = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text='Ship beam/width in meters'
    )

    height = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text='Ship height in meters'
    )

    mass = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text='Ship mass in kilograms'
    )

    # Crew & capacity
    crew_min = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text='Minimum crew required'
    )

    crew_max = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text='Maximum crew capacity'
    )

    cargo_capacity = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text='Cargo capacity in SCU (Standard Cargo Units)'
    )

    # Performance
    max_speed = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text='Maximum speed in m/s'
    )

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0'))],
        help_text='Price in aUEC (Alpha United Earth Credits)'
    )

    # Media
    image_url = models.URLField(
        max_length=500,
        blank=True,
        help_text='Primary ship image URL'
    )

    store_url = models.URLField(
        max_length=500,
        blank=True,
        help_text='RSI store page URL'
    )

    # Status flags
    is_flight_ready = models.BooleanField(
        default=False,
        db_index=True,
        help_text='Is ship currently flight-ready in game?'
    )

    is_concept = models.BooleanField(
        default=False,
        db_index=True,
        help_text='Is ship still in concept phase?'
    )

    # API metadata
    api_data = models.JSONField(
        default=dict,
        blank=True,
        help_text='Full API response data for reference'
    )

    last_updated = models.DateTimeField(
        auto_now=True,
        help_text='Last sync from Star Citizen API'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ships'
        verbose_name = 'Ship'
        verbose_name_plural = 'Ships'
        ordering = ['manufacturer__name', 'name']
        unique_together = [['manufacturer', 'model']]
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['type']),
            models.Index(fields=['size']),
            models.Index(fields=['is_flight_ready']),
            models.Index(fields=['manufacturer', 'name']),
        ]

    def __str__(self) -> str:
        """Return string representation of ship.

        Returns:
            str: Manufacturer and ship name
        """
        return f"{self.manufacturer.name} {self.name}"

    @property
    def full_name(self) -> str:
        """Get full ship name including manufacturer.

        Returns:
            str: Full ship designation
        """
        return f"{self.manufacturer.name} {self.model}"

    @property
    def status(self) -> str:
        """Get ship development status.

        Returns:
            str: Status string (Flight Ready, Concept, or In Development)
        """
        if self.is_flight_ready:
            return 'Flight Ready'
        elif self.is_concept:
            return 'Concept'
        return 'In Development'


class ShipComponent(models.Model):
    """
    Ship components like weapons, shields, power plants, etc.
    """

    # Component types
    TYPE_WEAPON = 'weapon'
    TYPE_SHIELD = 'shield'
    TYPE_POWER_PLANT = 'power_plant'
    TYPE_THRUSTER = 'thruster'
    TYPE_QUANTUM_DRIVE = 'quantum_drive'
    TYPE_COOLER = 'cooler'
    TYPE_SENSOR = 'sensor'
    TYPE_OTHER = 'other'

    TYPE_CHOICES = [
        (TYPE_WEAPON, 'Weapon'),
        (TYPE_SHIELD, 'Shield Generator'),
        (TYPE_POWER_PLANT, 'Power Plant'),
        (TYPE_THRUSTER, 'Thruster'),
        (TYPE_QUANTUM_DRIVE, 'Quantum Drive'),
        (TYPE_COOLER, 'Cooler'),
        (TYPE_SENSOR, 'Sensor'),
        (TYPE_OTHER, 'Other'),
    ]

    ship = models.ForeignKey(
        Ship,
        on_delete=models.CASCADE,  # Delete components when ship is deleted
        related_name='components',
        help_text='Ship this component belongs to'
    )

    type = models.CharField(
        max_length=50,
        choices=TYPE_CHOICES,
        db_index=True,
        help_text='Component type'
    )

    name = models.CharField(
        max_length=200,
        help_text='Component name/model'
    )

    size = models.CharField(
        max_length=20,
        blank=True,
        help_text='Component size classification (S1, S2, S3, etc.)'
    )

    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        help_text='Number of this component'
    )

    class Meta:
        db_table = 'ship_components'
        verbose_name = 'Ship Component'
        verbose_name_plural = 'Ship Components'
        ordering = ['ship', 'type', 'name']
        indexes = [
            models.Index(fields=['ship', 'type']),
            models.Index(fields=['type']),
        ]

    def __str__(self) -> str:
        """Return string representation of component.

        Returns:
            str: Component details
        """
        qty_str = f"{self.quantity}x " if self.quantity > 1 else ""
        return f"{qty_str}{self.name} ({self.get_type_display()})"
