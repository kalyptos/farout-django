"""
Sync ships from Star Citizen API to database.
Usage: python manage.py sync_ships [--force]
"""
from __future__ import annotations
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from apps.core.starcitizen_api import api_client, StarCitizenAPIError
from apps.starships.models import Manufacturer, Ship, ShipComponent
from typing import Any, Dict
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """Management command to sync ships from Star Citizen API."""

    help = 'Sync ships from Star Citizen API to database'

    def add_arguments(self, parser: Any) -> None:
        """Add command arguments.

        Args:
            parser: Argument parser
        """
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force update existing ships (default: only create new)',
        )
        parser.add_argument(
            '--clear-cache',
            action='store_true',
            help='Clear API cache before syncing',
        )

    def handle(self, *args: Any, **options: Any) -> None:
        """Execute the command.

        Args:
            *args: Positional arguments
            **options: Command options
        """
        force = options['force']
        clear_cache = options['clear_cache']

        if not api_client:
            raise CommandError(
                'Star Citizen API client not initialized. '
                'Check that STAR_CITIZEN_API_KEY is set in environment.'
            )

        self.stdout.write(self.style.MIGRATE_HEADING('🚀 Star Citizen Ship Sync'))
        self.stdout.write('=' * 60)

        if clear_cache:
            self.stdout.write('🗑️  Clearing API cache...')
            api_client.clear_cache('sc_api_ships*')

        try:
            # Fetch ships from API
            self.stdout.write('\n📡 Fetching ships from Star Citizen API...')
            ships_data = api_client.get_ships()

            if not ships_data:
                self.stdout.write(self.style.WARNING('⚠️  No ships returned from API'))
                return

            total_ships = len(ships_data) if isinstance(ships_data, list) else 0
            self.stdout.write(
                self.style.SUCCESS(f'✅ Fetched {total_ships} ships from API\n')
            )

            # Process each ship
            created_count = 0
            updated_count = 0
            skipped_count = 0
            error_count = 0

            for index, ship_data in enumerate(ships_data, 1):
                try:
                    result = self._sync_ship(ship_data, force)

                    if result == 'created':
                        created_count += 1
                        ship_name = ship_data.get('name', 'Unknown')
                        self.stdout.write(
                            f'  [{index}/{total_ships}] ✅ Created: {ship_name}'
                        )
                    elif result == 'updated':
                        updated_count += 1
                        ship_name = ship_data.get('name', 'Unknown')
                        self.stdout.write(
                            f'  [{index}/{total_ships}] 🔄 Updated: {ship_name}'
                        )
                    elif result == 'skipped':
                        skipped_count += 1

                except Exception as e:
                    error_count += 1
                    ship_name = ship_data.get('name', 'Unknown')
                    logger.error(f"Error syncing ship {ship_name}: {e}")
                    self.stdout.write(
                        self.style.ERROR(
                            f'  [{index}/{total_ships}] ❌ Error: {ship_name} - {str(e)[:50]}'
                        )
                    )

            # Summary
            self.stdout.write('\n' + '=' * 60)
            self.stdout.write(self.style.SUCCESS('✅ Ship sync complete!\n'))
            self.stdout.write(f'   📊 Total ships processed: {total_ships}')
            self.stdout.write(f'   ✨ Created: {created_count}')
            self.stdout.write(f'   🔄 Updated: {updated_count}')
            self.stdout.write(f'   ⏭️  Skipped: {skipped_count}')

            if error_count > 0:
                self.stdout.write(
                    self.style.ERROR(f'   ❌ Errors: {error_count}')
                )
            else:
                self.stdout.write('   ❌ Errors: 0')

        except StarCitizenAPIError as e:
            raise CommandError(f'API Error: {e}')
        except Exception as e:
            logger.exception("Unexpected error during ship sync")
            raise CommandError(f'Unexpected error: {e}')

    def _sync_ship(self, ship_data: Dict[str, Any], force: bool = False) -> str:
        """Sync a single ship to database.

        Args:
            ship_data: Ship data from API
            force: Whether to update existing ships

        Returns:
            str: Result status ('created', 'updated', or 'skipped')
        """
        with transaction.atomic():
            # Extract manufacturer data
            manufacturer_data = ship_data.get('manufacturer', {})
            manufacturer_code = manufacturer_data.get('code', 'UNK')
            manufacturer_name = manufacturer_data.get('name', 'Unknown')

            # Get or create manufacturer
            manufacturer, _ = Manufacturer.objects.get_or_create(
                code=manufacturer_code,
                defaults={
                    'name': manufacturer_name,
                    'description': manufacturer_data.get('description', ''),
                    'logo_url': manufacturer_data.get('logo', ''),
                    'api_data': manufacturer_data,
                }
            )

            # Extract ship fields
            ship_model = ship_data.get('model', ship_data.get('name', 'Unknown'))
            crew_data = ship_data.get('crew', {})
            media_data = ship_data.get('media', {})

            # Determine production status
            production_status = ship_data.get('production_status', '').lower()
            is_flight_ready = production_status == 'flight-ready'
            is_concept = production_status == 'concept'

            # Prepare ship defaults
            ship_defaults = {
                'name': ship_data.get('name', ''),
                'type': ship_data.get('type', ''),
                'size': self._normalize_size(ship_data.get('size', '')),
                'focus': ship_data.get('focus', ''),
                'description': ship_data.get('description', ''),
                'length': ship_data.get('length'),
                'beam': ship_data.get('beam'),
                'height': ship_data.get('height'),
                'mass': ship_data.get('mass'),
                'crew_min': crew_data.get('min') if isinstance(crew_data, dict) else None,
                'crew_max': crew_data.get('max') if isinstance(crew_data, dict) else None,
                'cargo_capacity': ship_data.get('cargo'),
                'max_speed': ship_data.get('max_speed'),
                'price': ship_data.get('price'),
                'image_url': media_data.get('image', '') if isinstance(media_data, dict) else '',
                'store_url': ship_data.get('store_url', ''),
                'is_flight_ready': is_flight_ready,
                'is_concept': is_concept,
                'api_data': ship_data,
            }

            # Get or create/update ship
            ship, created = Ship.objects.get_or_create(
                manufacturer=manufacturer,
                model=ship_model,
                defaults=ship_defaults
            )

            if created:
                return 'created'
            elif force:
                # Update existing ship
                for key, value in ship_defaults.items():
                    setattr(ship, key, value)
                ship.save()
                return 'updated'
            else:
                return 'skipped'

    def _normalize_size(self, size: str) -> str:
        """Normalize ship size to valid choice.

        Args:
            size: Size string from API

        Returns:
            str: Normalized size
        """
        size_lower = size.lower()

        # Map API sizes to model choices
        size_map = {
            'vehicle': 'vehicle',
            'snub': 'snub',
            'snub fighter': 'snub',
            'small': 'small',
            'medium': 'medium',
            'large': 'large',
            'capital': 'capital',
        }

        return size_map.get(size_lower, '')
