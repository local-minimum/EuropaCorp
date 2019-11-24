from typing import List

from mongodb.database import Database
from prometheus_client import Counter

from .mongogateway import (
    get_unprocessed_communications_per_user, get_user_profile,
    get_most_recent_storyid, update_profile, set_response,
    set_processed_communication, has_unprocessed_response,
    set_not_processed,
)
from .storygateway import StoryGateway
from .game import get_next_storyid_and_profile, compose_response
from .models import Communication
from .exceptions import UnknownMailerError


def get_mailer_from_bundle(bundle: List[Communication]) -> str:
    mailer = [
        communication.mailer for communication in bundle
        if communication.mailer
    ]
    if mailer:
        return mailer[0]
    raise UnknownMailerError("Unknown mailer, should not be possible")


def process_communication_bundle(
    db: Database,
    storygateway: StoryGateway,
    bundle: List[Communication],
    mailer: str, comm_counter: Counter,
):
    profile = get_user_profile(db, mailer)
    recent_storyid = get_most_recent_storyid(db, mailer)
    story = storygateway.get_story(recent_storyid)
    idxs = [communication.mongodb_id for communication in bundle]
    if story is None:
        set_not_processed(db, idxs)
        comm_counter.labels(
            recent_storyid if recent_storyid else '',
            'warning',
            'StoryMissing',
        ).inc()
        return
    next_storyid, profile = get_next_storyid_and_profile(
        bundle, story, profile,
    )
    if next_storyid:
        next_story = storygateway.get_story(next_storyid)
        response = compose_response(mailer, next_story, profile)
    else:
        set_not_processed(db, idxs)
        response = None
        comm_counter.labels(
            recent_storyid if recent_storyid else '',
            'warning',
            'NoValidStoryLink',
        ).inc()

    if response:
        set_response(db, response)
        set_processed_communication(
            db,
            [communication.mongodb_id for communication in bundle],
            next_storyid,
        )
        comm_counter.labels(
            next_storyid if next_storyid else '',
            'info',
            'Selected',
        )
    update_profile(db, profile)


def process_communications(
    db: Database, storygateway: StoryGateway, comm_counter: Counter,
):
    for bundle in get_unprocessed_communications_per_user(db):
        try:
            mailer = get_mailer_from_bundle(bundle)
        except UnknownMailerError:
            set_processed_communication(
                db, [communication.mongodb_id for communication in bundle],
            )
            comm_counter.labels('', 'error', 'UnknownMailerError').inc()
            continue
        if has_unprocessed_response(db, mailer) is True:
            idxs = [communication.mongodb_id for communication in bundle]
            set_not_processed(db, idxs)
            comm_counter.labels('', 'warning', 'Eagerness').inc()
            continue
        process_communication_bundle(
            db, storygateway, bundle, mailer, comm_counter,
        )
