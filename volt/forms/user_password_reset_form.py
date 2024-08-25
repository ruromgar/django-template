import logging

from django import forms
from django.contrib.auth.forms import PasswordResetForm


logger = logging.getLogger(__name__)


class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
