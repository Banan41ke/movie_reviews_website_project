from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = "Create admin user if not exists"

    def handle(self, *args, **kwargs):
        User = get_user_model()

        username = os.environ.get("DJANGO_ADMIN_USER")
        password = os.environ.get("DJANGO_ADMIN_PASSWORD")
        email = os.environ.get("DJANGO_ADMIN_EMAIL", "")

        if not username or not password:
            self.stdout.write("❌ Admin env vars not set")
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write("✅ Admin already exists")
            return

        User.objects.create_superuser(username, email, password)
        self.stdout.write("✅ Admin created")
