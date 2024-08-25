import logging

from django.contrib import messages
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpRequest
from django.shortcuts import redirect
from django.shortcuts import render

from home.agraph.agraph_models import GraphUser
from home.agraph.user_manager import UserManager
from volt.forms.registration_forms import RegistrationForm
from volt.models import InviteCode

logger = logging.getLogger(__name__)
user_manager = UserManager()


def register_view(request: HttpRequest):
    """Handle user registration.

    This view handles the registration of new users. It processes the registration form, validates the input,
    and creates a new user account. The registration form requires an email, password, and an invite code.

    Steps:
    1. If the request method is POST:
        - Make the POST data mutable.
        - Validate the invite code.
        - Assign the email as the username to bypass username validation.
        - Initialize the registration form with POST data.
        - If the form is valid:
            - Set the username to the email address.
            - Save the user to the database.
            - Refresh user data from the database.
            - Create a profile in the graph database using the user data.
            - Log the successful account creation.
            - Redirect the user to the login page.
        - If the form is not valid, log the form errors.
    2. If the request method is GET:
        - Initialize an empty registration form.
        - Check for the presence of an invite_code query parameter and prefill the invite code field if present.
    3. Render the registration page with the form.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered registration page with the form.
    """
    if request.method == "POST":
        invite_code = request.POST.get("invite_code")
        if not invite_code_is_valid(invite_code):
            messages.error(request, "Invalid invite code. Please try again.")
            return redirect("/accounts/register/")

        request.POST = request.POST.copy()
        request.POST["username"] = request.POST.get("email")
        form = RegistrationForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                form.instance.username = form.cleaned_data.get("email")
                user: User = form.save()
                user.refresh_from_db()
                create_graph_user(user=user)
                expire_invite_code(invite_code, user)
                logger.info(f"Account created for user {user.id}")
                # messages.success(request, "You have been successfully registered. Please log in")
                return redirect("/accounts/login/")
        else:
            logger.info(f"Registration failed: {form.errors.as_data()}")

    else:
        initial_data = {}
        invite_code = request.GET.get("invite_code")
        if invite_code:
            initial_data['invite_code'] = invite_code

        form = RegistrationForm(initial=initial_data)

    context = {"form": form}
    return render(request, "accounts/sign-up.html", context)


def invite_code_is_valid(invite_code: str) -> bool:
    """Validate the provided invite code.

    This function checks if the provided invite code is valid and active. It queries the InviteCode model to see if
    the code exists and is marked as active.

    Args:
        invite_code (str): The invite code to validate.

    Returns:
        bool: True if the invite code is valid and active, False otherwise.
    """
    try:
        code = InviteCode.objects.get(code=invite_code)
        return code.is_active
    except Exception as e:
        logger.info(f"Invite code {invite_code} is invalid: {e}")
        return False


def create_graph_user(user: User) -> None:
    user_manager.create_user(GraphUser(
        user_id=str(user.profile.graph_id),
        django_id=str(user.id),
        email=user.email
    ))


def expire_invite_code(invite_code: str, user: User) -> None:
    try:
        code = InviteCode.objects.get(code=invite_code)
        code.used_by = user
        code.is_active = False
        code.save()
    except Exception as e:
        logger.info(f"Invite code {invite_code} is invalid: {e}")
