"""
Item model for inventory management.
"""
from __future__ import annotations
from django.db import models
from django.core.validators import MinValueValidator


class Item(models.Model):
    """
    Generic item model for organization inventory.
    Tracks items with quantities and descriptions.
    """

    title = models.CharField(
        max_length=255,
        db_index=True,  # Add index for search performance
        help_text='Item name/title'
    )

    description = models.TextField(
        blank=True,
        null=True,
        help_text='Detailed item description'
    )

    quantity = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text='Available quantity (cannot be negative)'
    )

    image_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text='Item image URL'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'items'
        verbose_name = 'Item'
        verbose_name_plural = 'Items'
        ordering = ['title']
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self) -> str:
        """Return string representation of item.

        Returns:
            str: Item title with quantity
        """
        return f"{self.title} (x{self.quantity})"
