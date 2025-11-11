"""
Sync organization members from Star Citizen API.
Usage: python manage.py sync_org_members FAROUT
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.core.starcitizen_api import api_client, StarCitizenAPIError
from apps.organization.models import Organization, OrganizationMember
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Sync organization members from Star Citizen API'

    def add_arguments(self, parser):
        parser.add_argument(
            'sid',
            type=str,
            help='Organization SID (e.g., FAROUT)',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force update existing members',
        )

    def handle(self, *args, **options):
        sid = options['sid'].upper()
        force = options['force']

        self.stdout.write(f'👥 Syncing members for organization {sid}...')

        try:
            # Verify organization exists
            org = Organization.objects.filter(sid=sid).first()
            if not org:
                self.stdout.write(
                    self.style.WARNING(f'⚠️  Organization {sid} not found in database.')
                )
                self.stdout.write(f'   Run: python manage.py sync_organization {sid} first')
                return

            # Fetch members from API
            members_data = api_client.get_organization_members(sid)
            self.stdout.write(f'📦 Fetched {len(members_data)} members from API')

            created_count = 0
            updated_count = 0
            error_count = 0

            for member_data in members_data:
                try:
                    with transaction.atomic():
                        handle = member_data.get('handle', '').strip()
                        if not handle:
                            continue

                        member, created = OrganizationMember.objects.update_or_create(
                            handle=handle,
                            defaults={
                                'display_name': member_data.get('display_name', handle),
                                'rank': member_data.get('rank', ''),
                                'stars': member_data.get('stars', 0),
                                'avatar_url': member_data.get('image', ''),
                                'api_data': member_data,
                            }
                        )

                        if created:
                            created_count += 1
                            self.stdout.write(f'  ✅ Created: {member.handle}')
                        elif force:
                            updated_count += 1
                            self.stdout.write(f'  🔄 Updated: {member.handle}')

                except Exception as e:
                    error_count += 1
                    logger.error(f"Error syncing member {member_data.get('handle')}: {e}")
                    self.stdout.write(
                        self.style.ERROR(f'  ❌ Error: {member_data.get("handle")} - {e}')
                    )

            # Update organization member count
            org.member_count = OrganizationMember.objects.count()
            org.save(update_fields=['member_count'])

            self.stdout.write(self.style.SUCCESS(
                f'\n✅ Member sync complete!\n'
                f'   Created: {created_count}\n'
                f'   Updated: {updated_count}\n'
                f'   Errors: {error_count}\n'
                f'   Total members: {org.member_count}'
            ))

        except StarCitizenAPIError as e:
            self.stdout.write(self.style.ERROR(f'❌ API Error: {e}'))
