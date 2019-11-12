from typing import Optional
from pathlib import Path
from yaml import load, dump, YAMLError

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
        except IOError:
            return None
        except YAMLError:
            # TODO: Do some monitoring
            return None
        try:
            return Story.from_data(data)
        except StoryParsingError:
            # TODO: Do some monitoring
            pass
        return None
