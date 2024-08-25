import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.test import TestCase
from django.urls import reverse


class VoltAdminTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username="admin", password="supersecret"
        )
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="password123"
        )
        self.client = Client()

    @pytest.mark.django_db
    def test_user_admin_list_display(self):
        """Test that the custom list_display fields are shown in the User admin."""
        self.client.login(username="admin", password="supersecret")

        response = self.client.get(reverse("admin:auth_user_changelist"))
        assert response.status_code == 200
        assert "testuser" in response.content.decode()
        assert "testuser@example.com" in response.content.decode()
        assert "is_staff" in response.content.decode()

    @pytest.mark.django_db
    def test_profile_admin_search_fields(self):
        """Test that the search_fields in Profile admin work as expected."""
        self.client.login(username="admin", password="supersecret")
        response = self.client.get(
            reverse("admin:volt_profile_changelist") + "?q=testuser@example.com"
        )
        assert response.status_code == 200
        assert "testuser@example.com" in response.content.decode()
