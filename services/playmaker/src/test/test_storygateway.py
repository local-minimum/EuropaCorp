from pathlib import Path

import pytest

from playmaker import storygateway
from playmaker.dsl.tools import should_execute
from playmaker.models import Story, Communication


@pytest.fixture
def stories() -> Path:
    return Path(__file__).parent / 'fixtures'


def test_it_returns_a_story(stories):
    gw = storygateway.StoryGateway(stories)
    assert isinstance(gw.get_story("story"), Story)


def test_it_puts_the_title(stories):
    gw = storygateway.StoryGateway(stories)
    assert gw.get_story("story").title == "Some old text"


def test_it_puts_the_sender(stories):
    gw = storygateway.StoryGateway(stories)
    assert gw.get_story("story").sender == "happy@example.com"


def test_integration_link_test(stories):
    comm = Communication(
        mongodb_id="",
        mailer="me@hotmail.xcom",
        name="Me!",
        reciever="sad@example.com",
        body="I want yellow gold figs but not apples, oranges or bananas",
        medium="mail",
    )
    gw = storygateway.StoryGateway(stories)
    story = gw.get_story("story")
    assert [should_execute(link, comm) for link in story.links] == [
        False, True, True,
    ]
