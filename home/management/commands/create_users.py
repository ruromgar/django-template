import json
import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create a superuser with a predefined password if it does not exist"
    users_file = os.path.join(os.path.dirname(__file__), "../../fixtures/users.json")

    def handle(self, *args, **options):
        self.create_users()

    def create_users(self):
        with open(self.users_file, "r") as f:
            users = json.load(f)

        for user in users:
            if User.objects.filter(username=user["email"]).exists():
                self.stdout.write(
                    self.style.WARNING(f"User {user['email']} already exists")
                )
                continue

            if user["is_superuser"]:
                User.objects.create_superuser(
                    username=user["email"], email=user["email"], password=user["password"]
                )
            else:
                User.objects.create_user(
                    username=user["email"], email=user["email"], password=user["password"]
                )

            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully created user {user['email']}"
                )
            )
