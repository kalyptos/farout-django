"""
Django management command to wait for database availability.
Usage: python manage.py wait_for_db
"""
import time
from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError


class Command(BaseCommand):
    help = 'Wait for database to be available'

    def handle(self, *args, **options):
        """Wait for database."""
        self.stdout.write('Waiting for database...')
        db_conn = None
        retries = 0
        max_retries = 30

        while not db_conn and retries < max_retries:
            try:
                db_conn = connections['default']
                db_conn.cursor()
                self.stdout.write(self.style.SUCCESS('✓ Database available!'))
            except OperationalError:
                retries += 1
                self.stdout.write(
                    self.style.WARNING(f'Database unavailable, waiting 1 second... (attempt {retries}/{max_retries})')
                )
                time.sleep(1)

        if not db_conn:
            self.stdout.write(
                self.style.ERROR('✗ Could not connect to database after 30 attempts')
            )
            raise OperationalError('Database connection failed')
