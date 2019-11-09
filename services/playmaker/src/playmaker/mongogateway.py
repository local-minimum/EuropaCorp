from typing import List, Dict, Any, Optional, Iterable

from mongodb.database import Database

from .models import Profile, Communication, Response


def get_most_recent_storyid(db: Database, mailer: str) -> Optional[str]:
    return None


def get_unprocessed_communications_per_user(
    db: Database,
) -> Iterable[List[Communication]]:
    //TODO: Get the mails and stored interactions from the webpage
    // should only yeild bundles that contain something
    for _ in []:
        yield []


def get_user_profile(db: Database, user: str) -> Profile:
    return {}


def update_profile(db: Database, profile: Profile):
    pass


def set_reponse(db: Database, response: Response):
    pass


def set_processed_communication(db: Database, idxs: List[ObjectId]):
    pass
