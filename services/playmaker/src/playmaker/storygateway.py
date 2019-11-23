from typing import Optional
from pathlib import Path
from yaml import load, YAMLError
from prometheus_client import Counter
import logging

from .dsl.tools import build_rule
from .models import Story
from .exceptions import StoryParsingError


class StoryGateway:
    def __init__(self, basepath: Path, error_counter: Counter):
        self._basepath = basepath
        self._error_coutner = error_counter

    def get_story(self, story_id: Optional[str]) -> Optional[Story]:
        # No id is initial communication
        # No return Story is we're waiting for more content
        if story_id is None:
            story_id = 'start'
        path = self._basepath / "{}.yml".format(story_id)
        try:
            with open(path) as fs:
                data = load(fs)
        except IOError:
            self._error_coutner.labels(story_id, 'IOError').inc()
            logging.exception(
                'An error occurred reading story {} from {}'.format(
                    story_id, path,
                ),
            )
            return None
        except YAMLError:
            self._error_coutner.labels(story_id, 'YAMLError')
            logging.exception(
                'An error occurred reading story {} from {}'.format(
                    story_id, path,
                ),
            )
            return None
        try:
            story = Story.from_data(data, build_rule)
        except StoryParsingError:
            self._error_coutner.labels(story_id, 'StoryParsingError')
            logging.exception(
                'An error occurred reading story {} from {}'.format(
                    story_id, path,
                ),
            )
        else:
            return story
        return None
