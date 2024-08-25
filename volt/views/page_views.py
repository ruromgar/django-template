from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import redirect


@login_required(login_url="/accounts/login/")
def index(request: HttpRequest):
    # if request.user.profile.user_info:
    #     return redirect("profile", user_id=request.user.id)

    return redirect("cards")
