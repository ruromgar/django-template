from django.contrib.auth import views as auth_views
from django.urls import path

from volt.views import admin_views
from volt.views import authentication_views
from volt.views import error_views
from volt.views import page_views
from volt.views import registration_views


urlpatterns = [
    # Admin
    path('admin/generate_invite_codes/', admin_views.generate_invite_codes_view, name='generate_invite_codes'),

    # Index
    path("", page_views.index, name="index"),
    # Pages
    path("pages/dashboard/", page_views.dashboard, name="dashboard"),
    path("pages/transaction/", page_views.transaction, name="transaction"),
    path("pages/settings/", page_views.settings, name="settings"),
    # Tables
    path("tables/bs-tables/", page_views.bs_tables, name="bs_tables"),
    # Components
    path("components/buttons/", page_views.buttons, name="buttons"),
    path("components/notifications/", page_views.notifications, name="notifications"),
    path("components/forms/", page_views.forms, name="forms"),
    path("components/modals/", page_views.modals, name="modals"),
    path("components/typography/", page_views.typography, name="typography"),
    # Authentication
    path("accounts/register/", registration_views.register_view, name="register"),
    path("accounts/login/", authentication_views.UserLoginView.as_view(), name="login"),
    path("accounts/logout/", authentication_views.logout_view, name="logout"),
    path(
        "accounts/password-change/",
        authentication_views.UserPasswordChangeView.as_view(),
        name="password_change",
    ),
    path(
        "accounts/password-change-done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="accounts/password-change-done.html"
        ),
        name="password_change_done",
    ),
    path(
        "accounts/password-reset/",
        authentication_views.UserPasswordResetView.as_view(),
        name="password_reset",
    ),
    path(
        "accounts/password-reset-confirm/<uidb64>/<token>/",
        authentication_views.UserPasswrodResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "accounts/password-reset-done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/password-reset-done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "accounts/password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password-reset-complete.html"
        ),
        name="password_reset_complete",
    ),
    path("accounts/lock/", authentication_views.lock, name="lock"),

    # Errors
    path("error/404/", error_views.error_404, name="error_404"),
    path("error/500/", error_views.error_500, name="error_500"),
]
