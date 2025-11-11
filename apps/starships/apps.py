"""
Starships Django app configuration.
"""
from django.apps import AppConfig


class StarshipsConfig(AppConfig):
    """Configuration for the Starships app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.starships'
    verbose_name = 'Star Citizen Ships'

    def ready(self) -> None:
        """Import signals when app is ready."""
        # Import signals here if needed in the future
        pass
