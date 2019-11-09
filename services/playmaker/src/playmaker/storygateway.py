from typing import Optional
from pathlib import Path

from .models import Story


class StoryGateway:
    def __init__(self, basepath: Path):
        self._basepath = basepath

    def get_story(self, id: Optional[str]) -> Optional[Story]:
        # No id is initial communication
        return None
