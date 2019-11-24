from typing import Optional, Tuple, List
from collections import Counter
import re

from attr import evolve

from .models import Profile, Story, Communication, Response
from .dsl.tools import should_execute


def get_evolved_profile(
    bundle: List[Communication], profile: Profile,
):
    names = Counter(com.name for com in bundle if com.name)
    if names:
        name, count = names.most_common(1)[0]
        if count > 1 or not profile.name:
            profile = evolve(profile, name=name, evolved=True)
    return profile


def get_next_storyid_and_profile(
    bundle: List[Communication], story: Story, profile: Profile,
) -> Tuple[Optional[str], Profile]:
    for communication in bundle:
        for link in story.links:
            if should_execute(link, communication):
                return link.story_id, get_evolved_profile(bundle, profile)
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
    mailer: str, next_story: Optional[Story], profile: Profile,
) -> Optional[Response]:
    if not next_story:
        return None
    return Response(
        to=mailer,
        title=format_response(next_story.title, profile),
        body=format_response(next_story.body, profile),
        sender=next_story.sender,
    )
