"""
Starships models for managing Star Citizen ship data.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _


class Manufacturer(models.Model):
    """Ship manufacturers."""

    code = models.CharField(
        _('Code'),
        max_length=10,
        unique=True,
        help_text=_('Manufacturer code (e.g., AEGS)')
    )
    name = models.CharField(_('Name'), max_length=100)
    description = models.TextField(_('Description'), blank=True, null=True)
    logo_url = models.URLField(_('Logo URL'), blank=True)

    # API metadata
    api_id = models.CharField(_('API ID'), max_length=50, blank=True)
    api_data = models.JSONField(_('API Data'), default=dict, blank=True)

    # Timestamps
    created_at = models.DateTimeField(_('Created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated'), auto_now=True)

    class Meta:
        verbose_name = _('Manufacturer')
        verbose_name_plural = _('Manufacturers')
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class Ship(models.Model):
    """Star Citizen ships."""

    SIZE_CHOICES = [
        ('vehicle', _('Vehicle')),
        ('snub', _('Snub')),
        ('small', _('Small')),
        ('medium', _('Medium')),
        ('large', _('Large')),
        ('capital', _('Capital')),
    ]

    # Basic info
    name = models.CharField(_('Name'), max_length=200)
    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.PROTECT,
        related_name='ships',
        verbose_name=_('Manufacturer')
    )

    # Classification
    type = models.CharField(_('Type'), max_length=100, blank=True)
    size = models.CharField(
        _('Size'),
        max_length=20,
        choices=SIZE_CHOICES,
        default='small'
    )
    focus = models.CharField(_('Focus'), max_length=200, blank=True)

    # Description
    description = models.TextField(_('Description'), blank=True, null=True)
    career = models.CharField(_('Career'), max_length=100, blank=True)
    role = models.CharField(_('Role'), max_length=100, blank=True)

    # Technical specs
    length = models.DecimalField(
        _('Length (m)'),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    beam = models.DecimalField(
        _('Beam (m)'),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    height = models.DecimalField(
        _('Height (m)'),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    mass = models.DecimalField(
        _('Mass (kg)'),
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )

    # Crew
    min_crew = models.IntegerField(_('Min Crew'), null=True, blank=True)
    max_crew = models.IntegerField(_('Max Crew'), null=True, blank=True)

    # Cargo
    cargo_capacity = models.IntegerField(
        _('Cargo Capacity (SCU)'),
        null=True,
        blank=True
    )

    # Status
    is_flight_ready = models.BooleanField(_('Flight Ready'), default=False)
    is_concept = models.BooleanField(_('Concept'), default=False)
    production_status = models.CharField(
        _('Production Status'),
        max_length=50,
        blank=True
    )

    # Pricing
    pledge_price = models.DecimalField(
        _('Pledge Price (USD)'),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    # Media
    image_url = models.URLField(_('Image URL'), blank=True)
    store_url = models.URLField(_('Store URL'), blank=True)

    # API metadata
    api_id = models.CharField(
        _('API ID'),
        max_length=50,
        unique=True,
        blank=True
    )
    api_data = models.JSONField(_('API Data'), default=dict, blank=True)

    # Timestamps
    created_at = models.DateTimeField(_('Created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated'), auto_now=True)

    class Meta:
        verbose_name = _('Ship')
        verbose_name_plural = _('Ships')
        ordering = ['manufacturer__name', 'name']
        indexes = [
            models.Index(fields=['manufacturer', 'name']),
            models.Index(fields=['type']),
            models.Index(fields=['size']),
            models.Index(fields=['is_flight_ready']),
        ]

    def __str__(self) -> str:
        return f"{self.manufacturer.name} {self.name}"


class ShipComponent(models.Model):
    """Ship components and hardpoints."""

    COMPONENT_TYPE_CHOICES = [
        ('weapon', _('Weapon')),
        ('shield', _('Shield')),
        ('power', _('Power Plant')),
        ('cooler', _('Cooler')),
        ('quantum', _('Quantum Drive')),
        ('fuel', _('Fuel Tank')),
        ('cargo', _('Cargo Hold')),
        ('misc', _('Miscellaneous')),
    ]

    ship = models.ForeignKey(
        Ship,
        on_delete=models.CASCADE,
        related_name='components',
        verbose_name=_('Ship')
    )

    # Component info
    component_type = models.CharField(
        _('Type'),
        max_length=20,
        choices=COMPONENT_TYPE_CHOICES
    )
    name = models.CharField(_('Name'), max_length=200)
    size = models.CharField(_('Size'), max_length=10, blank=True)
    quantity = models.IntegerField(_('Quantity'), default=1)
    mount_name = models.CharField(_('Mount Name'), max_length=200, blank=True)

    # Details
    details = models.TextField(_('Details'), blank=True)
    api_data = models.JSONField(_('API Data'), default=dict, blank=True)

    # Timestamps
    created_at = models.DateTimeField(_('Created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated'), auto_now=True)

    class Meta:
        verbose_name = _('Ship Component')
        verbose_name_plural = _('Ship Components')
        ordering = ['ship', 'component_type', 'name']

    def __str__(self) -> str:
        return f"{self.ship.name} - {self.get_component_type_display()}: {self.name}"
