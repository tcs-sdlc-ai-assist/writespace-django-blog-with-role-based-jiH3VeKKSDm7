import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Creates the default admin superuser if not present.'

    def handle(self, *args, **options):
        username = os.environ.get('DEFAULT_ADMIN_USERNAME', 'admin')
        password = os.environ.get('DEFAULT_ADMIN_PASSWORD', 'admin')
        email = os.environ.get('DEFAULT_ADMIN_EMAIL', 'admin@example.com')

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(
                    f'Default admin user "{username}" already exists. Skipping creation.'
                )
            )
            return

        User.objects.create_superuser(
            username=username,
            password=password,
            email=email,
            is_staff=True,
            is_superuser=True,
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'Default admin user "{username}" created successfully.'
            )
        )