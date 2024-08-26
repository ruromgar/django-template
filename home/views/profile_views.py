import logging

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render


logger = logging.getLogger(__name__)


@login_required(login_url="/accounts/login/")
def profile(request, user_id: int):
    django_user = User.objects.get(id=user_id)
    context = {"profile": django_user.profile}
    return render(request, "profile.html", context)
