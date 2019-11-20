from typing import Optional
from pathlib import Path
from yaml import load, dump, YAMLError

from .dsl.tools import build_rule
from .models import Story
from .exceptions import StoryParsingError


class StoryGateway:
    def __init__(self, basepath: Path):
        self._basepath = basepath

    def get_story(self, id: Optional[str]) -> Optional[Story]:
        # No id is initial communication
        # No return Story is we're waiting for more content
        path = self._basepath / "{}.yml".format(id if id else "start")
        try:
            with open(path) as fs:
                data = load(fs)
        except IOError as e:
            print("ioerror {}".format(e))
            return None
        except YAMLError as e:
            # TODO: Do some monitoring
            print('YAMLError {}'.format(e))
            return None
        try:
            return Story.from_data(data, build_rule)
        except StoryParsingError as e:
            # TODO: Do some monitoring
            print('Parsing Error: {}'.format(e))
            pass
        return None
