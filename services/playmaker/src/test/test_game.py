import pytest

from playmaker import game
from playmaker import models


@pytest.mark.parametrize("text,profile,expect", (
    (
        "Hello {{profile.name}}!",
        models.Profile(mailer="test@hello.com", name="Me"),
        "Hello Me!",
    ),
    (
        "Hello {{ profile.name }}!",
        models.Profile(mailer="test@hello.com", name="You There"),
        "Hello You There!",
    ),
    (
        "Hello {{ profile.name }}!",
        models.Profile(mailer="test@hello.com"),
        "Hello {{ profile.name }}!",
    ),
))
def test_format_response(text, profile, expect):
    assert game.format_response(text, profile) == expect
