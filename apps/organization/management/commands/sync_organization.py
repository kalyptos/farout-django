"""
Sync organization from Star Citizen API.
Usage: python manage.py sync_organization FAROUT
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.core.starcitizen_api import api_client, StarCitizenAPIError
from apps.organization.models import Organization
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Sync organization from Star Citizen API'

    def add_arguments(self, parser):
        parser.add_argument(
            'sid',
            type=str,
            help='Organization SID (e.g., FAROUT)',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force update existing organization',
        )

    def handle(self, *args, **options):
        sid = options['sid'].upper()
        force = options['force']

        self.stdout.write(f'🏢 Syncing organization {sid}...')

        try:
            # Fetch organization from API
            org_data = api_client.get_organization(sid)

            if not org_data:
                self.stdout.write(self.style.ERROR(f'❌ Organization {sid} not found'))
                return

            self.stdout.write(f'📦 Fetched organization data from API')

            with transaction.atomic():
                # Check if organization exists
                org = Organization.objects.filter(sid=sid).first()

                defaults = {
                    'name': org_data.get('name', sid),
                    'url': org_data.get('url', ''),
                    'archetype': org_data.get('archetype', ''),
                    'commitment': org_data.get('commitment', ''),
                    'primary_language': org_data.get('primary_language', ''),
                    'recruiting': org_data.get('recruiting', False),
                    'member_count': org_data.get('member_count', 0),
                    'headline': org_data.get('headline', ''),
                    'description': org_data.get('description', ''),
                    'history': org_data.get('history', ''),
                    'manifesto': org_data.get('manifesto', ''),
                    'charter': org_data.get('charter', ''),
                    'logo_url': org_data.get('logo', ''),
                    'banner_url': org_data.get('banner', ''),
                    'api_data': org_data,
                }

                if org and force:
                    # Update existing organization
                    for key, value in defaults.items():
                        setattr(org, key, value)
                    org.save()
                    self.stdout.write(f'  🔄 Updated: {org.name} ({org.sid})')
                    action = 'updated'
                elif not org:
                    # Create new organization
                    org = Organization.objects.create(sid=sid, **defaults)
                    self.stdout.write(f'  ✅ Created: {org.name} ({org.sid})')
                    action = 'created'
                else:
                    self.stdout.write(f'  ⏭️  Skipped: Organization already exists (use --force to update)')
                    action = 'skipped'

            if action != 'skipped':
                self.stdout.write(self.style.SUCCESS(
                    f'\n✅ Organization sync complete!\n'
                    f'   Name: {org.name}\n'
                    f'   SID: {org.sid}\n'
                    f'   Members: {org.member_count}\n'
                    f'   Archetype: {org.archetype}\n'
                    f'   Action: {action}'
                ))

        except StarCitizenAPIError as e:
            self.stdout.write(self.style.ERROR(f'❌ API Error: {e}'))
