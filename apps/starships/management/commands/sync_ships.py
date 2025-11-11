"""
Sync ships from Star Citizen API.
Usage: python manage.py sync_ships
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.core.starcitizen_api import api_client, StarCitizenAPIError
from apps.starships.models import Manufacturer, Ship
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Sync ships from Star Citizen API'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force update existing ships',
        )

    def handle(self, *args, **options):
        force = options['force']

        self.stdout.write('🚀 Syncing ships from Star Citizen API...')

        try:
            # Fetch ships (manufacturers are embedded in ship data)
            self.stdout.write('🚢 Fetching ships from API...')
            ships_data = api_client.get_ships()
            self.stdout.write(f'📦 Fetched {len(ships_data)} ships from API')

            # Extract and create manufacturers from ship data
            self.stdout.write('📦 Extracting manufacturers from ship data...')
            manufacturers_seen = {}
            mfr_created = 0
            mfr_updated = 0

            for ship_data in ships_data:
                mfr_data = ship_data.get('manufacturer', {})
                code = mfr_data.get('code', '').strip()

                if code and code not in manufacturers_seen:
                    manufacturers_seen[code] = mfr_data
                    manufacturer, created = Manufacturer.objects.update_or_create(
                        code=code,
                        defaults={
                            'name': mfr_data.get('name', code),
                            'description': mfr_data.get('description', ''),
                            'api_id': str(mfr_data.get('id', '')),
                            'api_data': mfr_data,
                        }
                    )
                    if created:
                        mfr_created += 1
                    else:
                        mfr_updated += 1

            self.stdout.write(f'  ✅ Manufacturers: {mfr_created} created, {mfr_updated} updated')

            # Now sync ships
            self.stdout.write('🚢 Processing ships...')

            created_count = 0
            updated_count = 0
            skipped_count = 0
            error_count = 0

            for ship_data in ships_data:
                try:
                    with transaction.atomic():
                        # Get or create manufacturer
                        mfr_code = ship_data.get('manufacturer', {}).get('code', '').strip()
                        if not mfr_code:
                            skipped_count += 1
                            continue

                        manufacturer = Manufacturer.objects.filter(code=mfr_code).first()
                        if not manufacturer:
                            # Create manufacturer if not exists
                            manufacturer = Manufacturer.objects.create(
                                code=mfr_code,
                                name=ship_data.get('manufacturer', {}).get('name', mfr_code)
                            )

                        ship_name = ship_data.get('name', '').strip()
                        if not ship_name:
                            skipped_count += 1
                            continue

                        api_id = ship_data.get('id', '')

                        # Check if ship exists
                        if api_id:
                            ship = Ship.objects.filter(api_id=api_id).first()
                        else:
                            ship = Ship.objects.filter(
                                manufacturer=manufacturer,
                                name=ship_name
                            ).first()

                        defaults = {
                            'manufacturer': manufacturer,
                            'name': ship_name,
                            'type': ship_data.get('type', ''),
                            'size': ship_data.get('size', 'small').lower(),
                            'focus': ship_data.get('focus', ''),
                            'description': ship_data.get('description', ''),
                            'career': ship_data.get('career', ''),
                            'role': ship_data.get('role', ''),
                            'length': ship_data.get('length'),
                            'beam': ship_data.get('beam'),
                            'height': ship_data.get('height'),
                            'mass': ship_data.get('mass'),
                            'min_crew': ship_data.get('min_crew'),
                            'max_crew': ship_data.get('max_crew'),
                            'cargo_capacity': ship_data.get('cargo_capacity'),
                            'is_flight_ready': ship_data.get('production_status') == 'flight_ready',
                            'is_concept': ship_data.get('production_status') == 'concept',
                            'production_status': ship_data.get('production_status', ''),
                            'pledge_price': ship_data.get('pledge_price'),
                            'store_url': ship_data.get('store_url', ''),
                            'api_id': api_id,
                            'api_data': ship_data,
                        }

                        if ship and force:
                            # Update existing ship
                            for key, value in defaults.items():
                                setattr(ship, key, value)
                            ship.save()
                            updated_count += 1
                            self.stdout.write(f'  🔄 Updated: {manufacturer.code} {ship_name}')
                        elif not ship:
                            # Create new ship
                            ship = Ship.objects.create(**defaults)
                            created_count += 1
                            self.stdout.write(f'  ✅ Created: {manufacturer.code} {ship_name}')
                        else:
                            skipped_count += 1

                except Exception as e:
                    error_count += 1
                    logger.error(f"Error syncing ship {ship_data.get('name')}: {e}")
                    self.stdout.write(
                        self.style.ERROR(f'  ❌ Error: {ship_data.get("name")} - {e}')
                    )

            self.stdout.write(self.style.SUCCESS(
                f'\n✅ Ship sync complete!\n'
                f'   Created: {created_count}\n'
                f'   Updated: {updated_count}\n'
                f'   Skipped: {skipped_count}\n'
                f'   Errors: {error_count}\n'
                f'   Total ships in database: {Ship.objects.count()}'
            ))

        except StarCitizenAPIError as e:
            self.stdout.write(self.style.ERROR(f'❌ API Error: {e}'))
