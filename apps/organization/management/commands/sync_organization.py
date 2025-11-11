"""
Sync organization data from Star Citizen API.
Usage: python manage.py sync_organization <SID>
"""
from __future__ import annotations
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from apps.core.starcitizen_api import api_client, StarCitizenAPIError
from apps.organization.models import Organization
from typing import Any
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """Management command to sync organization from Star Citizen API."""

    help = 'Sync organization data from Star Citizen API'

    def add_arguments(self, parser: Any) -> None:
        """Add command arguments.

        Args:
            parser: Argument parser
        """
        parser.add_argument(
            'sid',
            type=str,
            help='Organization SID (e.g., FAROUT)',
        )

    def handle(self, *args: Any, **options: Any) -> None:
        """Execute the command.

        Args:
            *args: Positional arguments
            **options: Command options
        """
        sid = options['sid'].upper()

        if not api_client:
            raise CommandError(
                'Star Citizen API client not initialized. '
                'Check that STAR_CITIZEN_API_KEY is set in environment.'
            )

        self.stdout.write(self.style.MIGRATE_HEADING('🏢 Organization Sync'))
        self.stdout.write('=' * 60)
        self.stdout.write(f'\nOrganization SID: {sid}\n')

        try:
            # Fetch organization from API
            self.stdout.write('📡 Fetching organization data from API...')
            org_data = api_client.get_organization(sid)

            if not org_data:
                raise CommandError(f'No data returned for organization {sid}')

            # Sync to database
            with transaction.atomic():
                org, created = Organization.objects.update_or_create(
                    sid=sid,
                    defaults={
                        'name': org_data.get('name', sid),
                        'archetype': org_data.get('archetype', ''),
                        'commitment': org_data.get('commitment', ''),
                        'description': org_data.get('description', ''),
                        'member_count': org_data.get('members', 0),
                        'banner_url': org_data.get('banner', ''),
                        'logo_url': org_data.get('logo', ''),
                        'url': org_data.get('url', ''),
                        'api_data': org_data,
                    }
                )

                if created:
                    self.stdout.write(
                        self.style.SUCCESS(f'✅ Created organization: {org.name}')
                    )
                else:
                    self.stdout.write(
                        self.style.SUCCESS(f'🔄 Updated organization: {org.name}')
                    )

            # Display summary
            self.stdout.write('\n' + '=' * 60)
            self.stdout.write(self.style.SUCCESS('✅ Organization sync complete!\n'))
            self.stdout.write(f'   Name: {org.name}')
            self.stdout.write(f'   SID: {org.sid}')
            self.stdout.write(f'   Archetype: {org.archetype}')
            self.stdout.write(f'   Members: {org.member_count}')
            self.stdout.write(f'   RSI URL: {org.rsi_url}')

        except StarCitizenAPIError as e:
            raise CommandError(f'API Error: {e}')
        except Exception as e:
            logger.exception(f"Error syncing organization {sid}")
            raise CommandError(f'Error: {e}')
