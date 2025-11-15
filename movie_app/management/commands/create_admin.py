from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os

class Command(BaseCommand):
    help = 'Creates a default admin user if none exists'

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email=os.environ.get('ADMIN_EMAIL', 'admin@bitbox.com'),
                password=os.environ.get('ADMIN_PASSWORD', 'admin123')
            )
            self.stdout.write(
                self.style.SUCCESS('Successfully created admin user')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Admin user already exists')
            )