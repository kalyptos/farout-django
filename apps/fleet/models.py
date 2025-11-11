"""Fleet management models."""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class FleetShip(models.Model):
    """Ships owned by organization members."""

    STATUS_CHOICES = [
        ('active', _('Active')),
        ('pledged', _('Pledged')),
        ('loaned', _('On Loan')),
        ('sold', _('Sold')),
    ]

    ship = models.ForeignKey(
        'starships.Ship',
        on_delete=models.PROTECT,
        related_name='fleet_instances',
        verbose_name=_('Ship')
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_ships',
        verbose_name=_('Owner')
    )

    # Ownership details
    name = models.CharField(
        _('Custom Name'),
        max_length=200,
        blank=True,
        help_text=_('Custom ship name (optional)')
    )
    purchased_date = models.DateField(
        _('Purchased Date'),
        null=True,
        blank=True
    )
    status = models.CharField(
        _('Status'),
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )

    # Usage
    notes = models.TextField(_('Notes'), blank=True)
    is_available_for_missions = models.BooleanField(
        _('Available for Missions'),
        default=False
    )

    # Timestamps
    created_at = models.DateTimeField(_('Created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated'), auto_now=True)

    class Meta:
        verbose_name = _('Fleet Ship')
        verbose_name_plural = _('Fleet Ships')
        ordering = ['ship__manufacturer__name', 'ship__name']
        indexes = [
            models.Index(fields=['owner', 'status']),
            models.Index(fields=['ship', 'status']),
        ]

    def __str__(self) -> str:
        if self.name:
            return f"{self.name} ({self.ship.manufacturer.name} {self.ship.name})"
        return f"{self.ship.manufacturer.name} {self.ship.name} - {self.owner.username}"
