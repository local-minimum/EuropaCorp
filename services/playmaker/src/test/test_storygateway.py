from pathlib import Path

import pytest

from playmaker import storygateway
from playmaker.models import Story


@pytest.fixture
def stories() -> Path:
    return Path(__file__).parent / 'fixtures'


def test_it_returns_a_story(stories):
    gw = storygateway.StoryGateway(stories)
    assert isinstance(gw.get_story("story"), Story)
