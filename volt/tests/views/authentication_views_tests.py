from unittest import mock

import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.test import TestCase
from django.urls import reverse

from volt.forms.login_form import LoginForm
from volt.forms.user_password_change_form import UserPasswordChangeForm
from volt.forms.user_password_reset_form import UserPasswordResetForm


class AuthenticationViewsTests(TestCase):
    def setUp(self):
        """Set up reusable resources like the test client and a test user."""
        self.client = Client()
        self.user_password = "testpassword"
        self.test_user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password=self.user_password,
        )
        self.test_user.save()

    @pytest.mark.django_db
    def test_register_view(self):
        """Test the register view GET request."""
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/sign-up.html")
        # self.assertIsInstance(response.context["form"], RegistrationForm)

    @pytest.mark.django_db
    @mock.patch("volt.forms.AgraphManager")
    @mock.patch("home.agraph.user_manager.UserManager.create_user")
    def test_register_works_ok(
        self, mock_create_user: mock.MagicMock, mock_agraph: mock.MagicMock
    ):
        """Test the register view POST request for successful registration."""
        post_data = {
            "email": "newuser@example.com",
            "password1": "supersecret",
            "password2": "supersecret",
            "name": "New User",
            "organization": "test_org_id",
            "career_stage": "early_career_id",
            "phd_awarded_by": "some_university_id",
            "job_title": "Test Job Title",
            "seniority": "less_one_year",
            "research_focus_1": "Test Research Focus 1",
            "research_focus_2": "Test Research Focus 2",
        }
        response = self.client.post(reverse("register"), data=post_data)
        self.assertRedirects(response, "/accounts/login/")
        self.assertTrue(User.objects.filter(email="newuser@example.com").exists())
        self.assertTrue(mock_create_user.called)

    @pytest.mark.django_db
    @mock.patch("volt.forms.AgraphManager")
    @mock.patch("home.agraph.user_manager.UserManager.create_user")
    @mock.patch("volt.views.authentication_views.logger")
    def test_register_fails_if_not_all_required_fields_are_present(
        self,
        mock_logger: mock.MagicMock,
        mock_create_user: mock.MagicMock,
        mock_agraph: mock.MagicMock,
    ):
        """Test the register view POST request for successful registration."""
        post_data = {
            "email": "newuser@example.com",
            "password1": "supersecret",
            "password2": "supersecret",
            "name": "New User",
            "organization": "test_org_id",
            "career_stage": "early_career_id",
            "phd_awarded_by": "some_university_id",
            "seniority": "less_one_year",
            "research_focus_1": "Test Research Focus 1",
            "research_focus_2": "Test Research Focus 2",
        }
        self.client.post(reverse("register"), data=post_data)
        self.assertFalse(User.objects.filter(email="newuser@example.com").exists())
        self.assertFalse(mock_create_user.called)
        self.assertTrue(mock_logger.info.called)
        self.assertIn(
            "{'job_title': [ValidationError(['This field is required.'])]}",
            mock_logger.info.call_args[0][0],
        )

    @pytest.mark.django_db
    def test_login_view(self):
        """Test the login view."""
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/sign-in.html")
        self.assertIsInstance(response.context["form"], LoginForm)

    @pytest.mark.django_db
    def test_password_reset_view(self):
        """Test the password reset view GET request."""
        response = self.client.get(reverse("password_reset"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/forgot-password.html")
        self.assertIsInstance(response.context["form"], UserPasswordResetForm)

    @pytest.mark.django_db
    def test_password_change_view(self):
        """Test the password change view."""
        self.client.login(username=self.test_user.username, password=self.user_password)
        response = self.client.get(reverse("password_change"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/password-change.html")
        self.assertIsInstance(response.context["form"], UserPasswordChangeForm)

    @pytest.mark.django_db
    def test_logout_view(self):
        """Test the logout view."""
        self.client.login(username=self.test_user.username, password=self.user_password)
        response = self.client.get(reverse("logout"))
        self.assertRedirects(response, "/accounts/login/")
        self.assertNotIn("_auth_user_id", self.client.session)

    @pytest.mark.django_db
    def test_lock_view(self):
        """Test the lock view."""
        response = self.client.get(reverse("lock"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/lock.html")
