import json
import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from home.agraph.agraph_models import GraphUser
from home.agraph.user_manager import UserManager


class Command(BaseCommand):
    help = "Create a superuser with a predefined password if it does not exist"
    users_file = os.path.join(os.path.dirname(__file__), "../../fixtures/users.json")

    def handle(self, *args, **options):
        self.create_users()

    def create_users(self):
        with open(self.users_file, "r") as f:
            users = json.load(f)

        um = UserManager()
        for user in users:
            if not User.objects.filter(username=user["email"]).exists():
                django_user: User
                if user["is_superuser"]:
                    django_user = User.objects.create_superuser(
                        username=user["email"], email=user["email"], password=user["password"]
                    )
                else:
                    django_user = User.objects.create_user(
                        username=user["email"], email=user["email"], password=user["password"]
                    )
                if user.get("user_info"):
                    django_user.profile.user_info = user["user_info"]
                    django_user.profile.save()
                if user.get("pretty_printed"):
                    django_user.profile.pretty_printed_user_info = user["pretty_printed"]
                    django_user.profile.save()

                user["user_id"] = str(django_user.profile.graph_id)
                user["django_id"] = str(django_user.id)
                um.create_user(GraphUser.from_dict(user))  # type: ignore
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully created user {user['email']}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"User {user['email']} already exists")
                )
