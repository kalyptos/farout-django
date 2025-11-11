"""
Django management command to create default admin user.
Usage: python manage.py create_default_admin
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from decouple import config

User = get_user_model()


class Command(BaseCommand):
    help = 'Create default admin user if not exists'

    def handle(self, *args, **options):
        """Create default admin user."""

        # Get credentials from environment - no defaults for security
        username = config('DEFAULT_ADMIN_USERNAME', default='admin')
        email = config('DEFAULT_ADMIN_EMAIL', default='admin@farout.com')

        # SECURITY: Password MUST be set in environment variable
        try:
            password = config('DEFAULT_ADMIN_PASSWORD')
        except Exception:
            self.stdout.write(
                self.style.ERROR(
                    '❌ ERROR: DEFAULT_ADMIN_PASSWORD environment variable must be set.\n'
                    '   For security reasons, no default password is provided.\n'
                    '   Set it in your .env file or environment variables.'
                )
            )
            return

        # Check if admin user already exists
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'Admin user "{username}" already exists. Skipping creation.')
            )
            return

        # Create admin user
        admin_user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            role=User.ROLE_ADMIN,
            is_active=True,
            is_staff=True,
            is_superuser=True
        )

        self.stdout.write(
            self.style.SUCCESS(f'✓ Successfully created admin user: {username}')
        )
        self.stdout.write(
            self.style.SUCCESS(f'  Username: {username}')
        )
        # SECURITY: Never log passwords
        self.stdout.write(
            self.style.WARNING('  ⚠️  SECURITY: Change the default admin password immediately after first login!')
        )
