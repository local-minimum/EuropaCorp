from typing import Optional, Dict, Tuple

from .models import Profile, Story, Communication, Response


def get_next_storyid_and_profile(
    bundle: List[Communication], story: Story, profile: Profile,
) -> Tuple[Optional[str], Dict[str, Any]]:
    return None, profile


def compose_response(
    mailer: str, next_story: Story, profile: Profile,
) -> Response:
    return Response() 
