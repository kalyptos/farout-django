"""
Item model for inventory management.
"""
from django.db import models


class Item(models.Model):
    """
    Generic item model for organization inventory.
    """

    title = models.CharField(
        max_length=255,
        help_text='Item name/title'
    )

    description = models.TextField(
        blank=True,
        null=True,
        help_text='Item description'
    )

    quantity = models.IntegerField(
        default=0,
        help_text='Available quantity'
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

    def __str__(self):
        return f"{self.title} (x{self.quantity})"
