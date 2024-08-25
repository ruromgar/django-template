from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class PageViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="user@example.com", password="testpassword"
        )

    def test_index_view_status_code(self):
        """Test that the index view returns a 200 HTTP status code."""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/index.html")
