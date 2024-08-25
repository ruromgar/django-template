from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class ErrorViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="user@example.com", password="testpassword"
        )

    def test_error_404(self):
        """Test that the 404 error view returns the right template."""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("error_404"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "errors/404.html")

    def test_error_500(self):
        """Test that the 500 error view returns the right template."""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("error_500"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "errors/500.html")
