import json
import logging
from typing import Any
from typing import Dict
from typing import Optional

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render

from home.agraph.agraph_manager import AgraphManager
from home.agraph.agraph_models import InstanceWithLabel
from home.agraph.user_manager import UserManager
from home.constants import card_constants
from home.constants import profile_constants as constants
from home.views.utils import decode_uri
from home.views.utils import encode_uri
from home.views.utils import get_card_context
from home.views.utils import get_label_from_uri
from home.views.utils import get_readonly_context

logger = logging.getLogger(__name__)
user_manager = UserManager()
agraph_manager = AgraphManager()


@login_required(login_url="/accounts/login/")
def profile(request, user_id: int):
    django_user = User.objects.get(id=user_id)
    context = _get_user_context(
        django_id=user_id,
        graph_id=str(django_user.profile.graph_id)
    )
    return render(request, "profile.html", context)


@login_required(login_url="/accounts/login/")
def fetch_card_data_for_user(request, card_id: str, user_id: int):
    card = agraph_manager.get_card_details(card_id=decode_uri(card_id))
    if not card:
        raise Http404("Card not found")

    template = card_constants.CARD_TYPE_READONLY_TEMPLATE_MAPPING.get(card.card_type)
    if not template:
        raise Http404("Template not found")

    context = get_card_context(card, user_manager, agraph_manager)
    return render(request, template, context=get_readonly_context(context))


def _get_user_context(django_id: int, graph_id: str):
    try:
        django_user = User.objects.get(id=django_id)
    except User.DoesNotExist:
        raise Http404("User not found")

    contributions = user_manager.get_user_contributions(graph_id)
    for c in contributions:
        c.id = encode_uri(c.id)
    tagged_in_cards = _get_tagged_in_cards(contributions)
    taggers = _get_taggers(contributions)

    # We only want to show public cards
    activities = [a for a in user_manager.get_user_activities(graph_id) if a.is_public == "yes"]
    for a in activities:
        a.id = encode_uri(a.id)

    created_cards = _get_user_creations(graph_id)

    profile_data = django_user.profile.pretty_printed_user_info or {}
    context: Dict[str, Any] = {
        "segment": "profile",
        "profile_unclaimed": profile_data == {},
        "user_id": django_id,
        "name": profile_data.get(constants.PF_NAME),
        "job_title": profile_data.get(constants.PF_JOB_TITLE),
        "employer": profile_data.get(constants.PF_EMPLOYER),
        "workplace": profile_data.get(constants.PF_PLACE_OF_WORK),
        "career_stage": profile_data.get(constants.PF_CAREER_STAGE),
        "thesis_data": profile_data.get(constants.PF_THESIS_DATA),
        "at_a_glance": _get_at_a_glance(profile_data),
        "working_on": profile_data.get(constants.PF_WORKING_ON),
        "upcoming": profile_data.get(constants.PF_UPCOMING_OPPORTUNITIES),
        "have_done": profile_data.get(constants.PF_HAVE_DONE),
        "primary_contact_for": profile_data.get(constants.PF_PRIMARY_CONTACT_FOR),
        "affiliations": profile_data.get(constants.PF_AFFILIATIONS),
        "studies": profile_data.get(constants.PF_STUDIES),
        "methods": profile_data.get(constants.PF_METHODS),
        "topics": profile_data.get(constants.PF_TOPICS),
        "groups": profile_data.get(constants.PF_GROUPS),
        "skillset": profile_data.get(constants.PF_SKILLSET),
        "lab_group": profile_data.get(constants.PF_COLLABORATORS),
        "user_contributions": _get_chart_pie_data(created_cards),
        "taggers": taggers,
        "activity_log": activities,
        "created_cards": created_cards,
        "tagged_in_cards": tagged_in_cards,
        "links": profile_data.get(constants.PF_CONTACT_LINKS),
    }

    return context


def _get_user_creations(user_id: str) -> dict[str, list[InstanceWithLabel]]:
    cards = user_manager.get_user_creations(user_id)
    for c in cards:
        c.id = encode_uri(c.id)

    cards_by_type: dict[str, list[InstanceWithLabel]] = dict()
    for card in cards:
        # We only want to show public, non-stub cards
        if card.is_public != "yes" or card.is_stub == "yes":
            continue

        assert card.type is not None
        if card.type not in cards_by_type.keys():
            cards_by_type[card.type] = [card]
        else:
            cards_by_type[card.type].append(card)

    return cards_by_type


def _get_tagged_in_cards(cards: list[InstanceWithLabel]) -> dict[str, list[InstanceWithLabel]]:
    cards_by_type: dict[str, list[InstanceWithLabel]] = dict()
    for card in cards:
        # We only want to show public, non-stub cards
        if card.is_public != "yes" or card.is_stub == "yes":
            continue

        assert card.type is not None
        if card.type not in cards_by_type.keys():
            cards_by_type[card.type] = [card]
        else:
            cards_by_type[card.type].append(card)

    return cards_by_type


def _get_taggers(cards: list[InstanceWithLabel]) -> dict[tuple[str, str], list[InstanceWithLabel]]:
    cards_by_tagger: dict[str, list[InstanceWithLabel]] = dict()
    for card in cards:
        # We only want to show public, non-stub cards
        if card.is_public != "yes" or card.is_stub == "yes":
            continue

        assert card.created_by is not None
        creator = get_label_from_uri(card.created_by)
        if creator not in cards_by_tagger.keys():
            cards_by_tagger[creator] = [card]
        else:
            cards_by_tagger[creator].append(card)

    taggers_info: dict[tuple[str, str], list[InstanceWithLabel]] = {}
    for tagger, cards in cards_by_tagger.items():
        tagger_details = user_manager.get_user_details(tagger)
        taggers_info[(tagger_details.email, tagger_details.django_id)] = cards

    return taggers_info


def _get_chart_pie_data(cards: dict[str, list[InstanceWithLabel]]) -> str:
    total = sum(len(v) for v in cards.values())
    return json.dumps({k: round((len(v) / total) * 100) for k, v in cards.items()})


def _get_at_a_glance(data: dict[str, Any]) -> Optional[str]:
    summary_parts = []

    if cs := data.get(constants.PF_CAREER_STAGE):
        summary_parts.append(f'{cs}')

    if jt := data.get(constants.PF_JOB_TITLE):
        job_title_part = f' working as a {jt}' if summary_parts else f'{jt}'
        summary_parts.append(job_title_part)

    if e := data.get(constants.PF_EMPLOYER):
        employer_part = f'at {e}.' if summary_parts else f'Working at {e}.'
        summary_parts.append(employer_part)

    return ' '.join(summary_parts) if summary_parts else None
