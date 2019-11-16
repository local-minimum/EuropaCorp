import pytest

from playmaker import game
from playmaker import models


def mkcommunication(
    mongodb_id="aaaaaa",
    mailer="hello@world.org",
    name="Hello Me",
    reciever="support@euco.com",
    body="What is this crap?",
    medium="mail",
):
    return models.Communication(
        mongodb_id=mongodb_id, mailer=mailer, name=name, reciever=reciever,
        body=body, medium=medium,
    )


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


class TestGetEvolvedProfile:
    def test_applies_name(self):
        profile = models.Profile(mailer="me@me.me")
        bundle = [mkcommunication(name="I am Name")]
        assert game.get_evolved_profile(bundle, profile) == models.Profile(
            name="I am Name",
            mailer="me@me.me",
        )

    def test_updates_name_if_probable(self):
        profile = models.Profile(mailer="me@me.me", name='Dot')
        bundle = [
            mkcommunication(name="I am Name"), mkcommunication(name="I am Name"),
            mkcommunication(name="Dot"),
        ]
        assert game.get_evolved_profile(bundle, profile) == models.Profile(
            name="I am Name",
            mailer="me@me.me",
        )

    def test_keeps_name(self):
        profile = models.Profile(mailer="me@me.me", name="Dot")
        bundle = [mkcommunication(name="I am Name")]
        assert game.get_evolved_profile(bundle, profile) == models.Profile( 
            name="Dot",
            mailer="me@me.me",
        )
