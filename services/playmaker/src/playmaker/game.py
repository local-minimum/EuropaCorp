from typing import Optional, Dict, Tuple, List, Any
from collections import Counter
import re

from attr import evolve

from .models import Profile, Story, Communication, Response


def get_evolved_profile(
    bundle: List[Communication], profile: Profile,
):
    names = Counter(com.name for com in bundle if com.name)
    if names:
        name, count = names.most_common(1)[0]
        if count > 1 or not profile.name:
            profile = evolve(profile, name=name)
    return profile


def get_next_storyid_and_profile(
    bundle: List[Communication], story: Story, profile: Profile,
) -> Tuple[Optional[str], Dict[str, Any]]:
    return None, get_evolved_profile(bundle, profile)


def format_response(text: str, profile: Profile) -> str:
    for prop in ('name',):
        if isinstance(getattr(profile, prop), str):
            text = re.sub(
                r"{{ ?profile\." + prop + r" ?}}",
                getattr(profile, prop),
                text,
            )
    return text


def compose_response(
    mailer: str, next_story: Story, profile: Profile,
) -> Response:
    return Response(
        to=mailer,
        title=format_response(next_story.title, profile),
        body=format_response(next_story.body, profile),
        sender=next_story.sender,
    )
