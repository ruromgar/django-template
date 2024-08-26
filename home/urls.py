from django.urls import path

from home.views import profile_views

urlpatterns = [
    path("profile/<int:user_id>/", profile_views.profile, name="profile"),
]
