from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = 'Creates a default admin user if none exists'

    def handle(self, *args, **options):
        User = get_user_model()
        username = 'admin'
        email = 'admin@bitbox.com'
        password = os.environ.get('ADMIN_PASSWORD', 'admin123')
        
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password)
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created admin user: {username}')
            )
        else:
            # Update password if user exists
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            self.stdout.write(
                self.style.SUCCESS(f'Updated password for admin user: {username}')
            )