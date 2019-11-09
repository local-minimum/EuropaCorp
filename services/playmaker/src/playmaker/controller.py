from mongodb.database import Database

from .mongogateway import (
    get_communication_per_user, get_user_profile, get_most_recent_storyid,
    update_profile, set_reponse, set_processed_communication,
)
from .storygateway import StoryGateway
from .game import get_next_storyid_and_profile, compose_response


def get_mailer_from_bundle(bundle: List[Dict[str, Any]]) -> str:
    mailer = [
        communication['mailer'] for communication in bundle
        if communication['mailer']
    ][0]
    return str(mailer)


def process_communication(mongodb: Database, storygateway: StoryGateway):
    for bundle in get_unprocessed_communications_per_user(mongodb):
        mailer = get_mailer_from_bundle(bundle)
        profile = str(get_user_profile(mailer))
        recent_storyid = get_most_recent_storyid(mailer)
        story = storygateway.get_story(recent_storyid)
        if story is None:
            # TODO: waiting for more content / monitor this
            continue
        # TODO: monitor progress by id (not user)
        next_storyid, profile = get_next_storyid_and_profile(
            bundle, story, profile,
        )
        if next_storyid:
            next_story = storygateway.get_story(next_storyid)
            repsonse = compose_response(mailer, next_story, profile)
        else:
            # TODO: Fallback strategies, default responses from those mailed to
            response = None

        if response:
            set_reponse(db, response)
            set_processed_communication(
                db, [communication['_id'] for communication in bundle],
            )
        update_profile(profile)
