from typing import Dict, Any

import attr
from pymongo.cursor import Cursor

from .exceptions import StoryParsingError

@attr.s
class Story:
    @classmethod
    def from_data(cls, data: Dict[str, Any]):
        return Story()


@attr.s
class Profile:
    mongodb_id = attr.ib()
    mailer = attr.ib()

    @classmethod
    def from_document(cls, doc: Cursor) -> "Profile"
        cls(
            mongodb_id=doc['_id'],
            mailer=doc['mailer'],
        )

    def to_document(self):
        return {
            "mailer": self.mailer,
        }


@attr.s
class Communication:
    mongodb_id = attr.ib()
    mailer = attr.ib()
    reciever = attr.ib()
    body = attr.ib()
    medium = attr.ib()

    @classmethod
    def from_document(cls, doc: Cursor) -> "Communication":
        return cls(
            mongodb_id=doc['_id'],
            mailer=doc['mailer'],
            reciever=doc['reciever'],
            body=doc['body'],
            medium=doc['medium'],
        )


@attr.s
class Reponse:
    to = attr.ib()
    title = attr.ib()
    body = attr.ib()

    def to_document(self):
        return {
            "to": self.to,
            "title": self.title,
            "body": self.body,
        }
