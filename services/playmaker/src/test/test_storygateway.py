from pathlib import Path

import pytest
from unittest.mock import Mock

from playmaker import storygateway
from playmaker.dsl.tools import should_execute
from playmaker.models import Story, Communication


@pytest.fixture
def stories() -> Path:
    return Path(__file__).parent / 'fixtures'


def test_it_returns_a_story(stories):
    counter = Mock()
    gw = storygateway.StoryGateway(stories, counter)
    assert isinstance(gw.get_story("story"), Story)
    counter.labels.assert_not_called()


def test_it_handles_missing_stories(stories):
    counter = Mock()
    gw = storygateway.StoryGateway(stories, counter)
    assert gw.get_story("no_story") is None
    counter.labels.assert_called_with("no_story", "IOError")


def test_it_handles_bad_yaml(stories):
    counter = Mock()
    gw = storygateway.StoryGateway(stories, counter)
    assert gw.get_story("badyaml_story") is None
    counter.labels.assert_called_with("badyaml_story", "YAMLError")


def test_it_handles_bad_story(stories):
    counter = Mock()
    gw = storygateway.StoryGateway(stories, counter)
    assert gw.get_story("bad_story") is None
    counter.labels.assert_called_with("bad_story", "StoryParsingError")


def test_it_puts_the_title(stories):
    counter = Mock()
    gw = storygateway.StoryGateway(stories, counter)
    assert gw.get_story("story").title == "Some old text"


def test_it_puts_the_sender(stories):
    counter = Mock()
    gw = storygateway.StoryGateway(stories, counter)
    assert gw.get_story("story").sender == "happy@example.com"


def test_integration_link_test(stories):
    counter = Mock()
    comm = Communication(
        mongodb_id="",
        mailer="me@hotmail.xcom",
        name="Me!",
        reciever="sad@example.com",
        body="I want yellow gold figs but not apples, oranges or bananas",
        medium="mail",
    )
    gw = storygateway.StoryGateway(stories, counter)
    story = gw.get_story("story")
    assert [should_execute(link, comm) for link in story.links] == [
        False, True, True,
    ]
