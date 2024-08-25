import logging

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UsernameField
from django.utils.translation import gettext_lazy as _


logger = logging.getLogger(__name__)


class LoginForm(AuthenticationForm):
    username = UsernameField(
        label=_("Your email"),
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Email"}),
    )
    password = forms.CharField(
        label=_("Your Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        ),
    )
