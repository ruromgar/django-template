# from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render
from django.utils.crypto import get_random_string

from volt.forms.admin_forms import GenerateInviteCodesForm
from volt.models import InviteCode


@login_required(login_url="/accounts/login/")
def generate_invite_codes_view(request: HttpRequest):
    if request.method == "POST":
        form = GenerateInviteCodesForm(request.POST)
        if form.is_valid():
            source_event = form.cleaned_data['source_event']
            num_codes = form.cleaned_data['num_codes']
            expires_at = form.cleaned_data['expires_at']
            created_by = request.user

            codes = []
            for _ in range(num_codes):
                code = InviteCode.objects.create(
                    source_event=source_event,
                    created_by=created_by,
                    expires_at=expires_at,
                    code=get_random_string(15)
                )
                codes.append(code.code)

            # messages.success(request, "Invite codes generated successfully!")
            return render(request, 'admin/invite_codes_generated.html', {'codes': codes})

    else:
        form = GenerateInviteCodesForm()

    return render(request, 'admin/generate_invite_codes.html', {'form': form})
