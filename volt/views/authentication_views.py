import logging

from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.views import PasswordResetView
from django.shortcuts import redirect
from django.shortcuts import render

from volt.forms.login_form import LoginForm
from volt.forms.user_password_change_form import UserPasswordChangeForm
from volt.forms.user_password_reset_form import UserPasswordResetForm
from volt.forms.user_password_set_form import UserSetPasswordForm

logger = logging.getLogger(__name__)


class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = "accounts/sign-in.html"


class UserPasswordChangeView(PasswordChangeView):
    template_name = "accounts/password-change.html"
    form_class = UserPasswordChangeForm


class UserPasswordResetView(PasswordResetView):
    template_name = "accounts/forgot-password.html"
    form_class = UserPasswordResetForm


class UserPasswrodResetConfirmView(PasswordResetConfirmView):
    template_name = "accounts/reset-password.html"
    form_class = UserSetPasswordForm


def logout_view(request):
    logout(request)
    return redirect("/accounts/login/")


def lock(request):
    return render(request, "accounts/lock.html")
