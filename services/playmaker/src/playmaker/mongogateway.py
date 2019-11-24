import datetime as dt
from typing import List, Optional, Iterable

from pymongo import ASCENDING, DESCENDING, ObjectId
from mongodb.database import Database

from .models import Profile, Communication, Response

MAILS = 'mails'
PROFILES = 'profiles'
RESPONSE = 'response'


def get_most_recent_storyid(db: Database, mailer: str) -> Optional[str]:
    res = db[MAILS].find(
        {
            "processed_time": {"$exists": True},
            "story_id": {"$exists": True},
            "mailer": mailer,
        },
    ).sort(
        {"processed_time": DESCENDING},
    ).limit(1)
    if res:
        return res['story_id']
    return None


def get_unprocessed_communications_per_user(
    db: Database,
) -> Iterable[List[Communication]]:
    retry_threshold = dt.datetime.utcnow() - dt.timedelta(days=3)
    inclusion_filter = {"$and": [
        {"processed_time": None},
        {"$or": [
            {"not_found_time": {"$exists": False}},
            {"not_found_time": {"$gt": retry_threshold}},
        ]},
    ]}
    mailers = set(
        doc['mailer'] for doc in
        db[MAILS].find(inclusion_filter, {"_id": 0, "mailer": 1})
    )
    for mailer in mailers:
        yield [
            Communication.from_document(doc)
            for doc in db[MAILS].find(
                {"$and": [inclusion_filter, {"mailer": mailer}]}
            ).sort(
                'created_time', ASCENDING,
            )
        ]


def set_not_processed(db: Database, idxs: List[ObjectId]):
    not_found_time = dt.datetime.utcnow()
    db[MAILS].update(
        {'_id': {"$in": idxs}},
        {"$set": {"not_found_time": not_found_time}},
    )


def get_user_profile(db: Database, user: str) -> Profile:
    document = db[PROFILES].find_one({"mailer": user})
    if document:
        Profile.from_document(document)
    return Profile(mongodb_id=None, mailer=user)


def update_profile(db: Database, profile: Profile):
    if profile.mongodb_id:
        if profile.evolved:
            db[PROFILES].find_one_and_update(
                {"_id": profile.mongodb_id},
                {"$set": profile.to_document()},
            )
    else:
        db[PROFILES].insert_one(profile.to_document())


def has_unprocessed_response(db: Database, user: str) -> bool:
    return (
        db[RESPONSE].find_one({"to": user, "sent": {"$exists": False}})
        is not None
    )


def set_response(db: Database, response: Response):
    db[RESPONSE].insert_one(response.to_document())


def set_processed_communication(
    db: Database, idxs: List[ObjectId], story_id: Optional[str] = None,
):
    processed_time = dt.datetime.utcnow()
    db[MAILS].update(
        {'_id': {"$in": idxs}},
        {"$set": {"processed_time": processed_time, "story_id": story_id}},
    )
