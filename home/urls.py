from django.urls import path

from home.views import profile_views

urlpatterns = [
    path("", views.index, name="index"),
    path("profile/<int:user_id>/", profile_views.profile, name="profile"),
]
