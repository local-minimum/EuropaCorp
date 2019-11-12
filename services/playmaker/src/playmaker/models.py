from typing import Dict, Any

import attr
from pymongo.cursor import Cursor

from .exceptions import StoryParsingError


@attr.s
class Story:
    title = attr.ib()
    sender = attr.ib()
    body = attr.ib()

    @classmethod
    def from_data(cls, data: Dict[str, Any]):
        try:
            return Story(
                title=data['title'],
                sender=data['sender'],
                body=data['body'],
            )
        except KeyError:
            raise StoryParsingError("Malformatted yml")


@attr.s
class Profile:
    mailer = attr.ib()
    mongodb_id = attr.ib(default=None)
    name = attr.ib(default=None)

    @classmethod
    def from_document(cls, doc: Cursor) -> "Profile":
        cls(
            mongodb_id=doc['_id'],
            mailer=doc['mailer'],
            name=doc['name'],
        )

    def to_document(self):
        return {
            "mailer": self.mailer,
            "name": self.name,
        }


@attr.s
class Communication:
    mongodb_id = attr.ib()
    mailer = attr.ib()
    name = attr.ib()
    reciever = attr.ib()
    body = attr.ib()
    medium = attr.ib()

    @classmethod
    def from_document(cls, doc: Cursor) -> "Communication":
        return cls(
            mongodb_id=doc['_id'],
            mailer=doc['mailer'],
            name=doc['name'],
            reciever=doc['reciever'],
            body=doc['body'],
            medium=doc['medium'],
        )


@attr.s
class Response:
    to = attr.ib()
    title = attr.ib()
    body = attr.ib()
    sender = attr.ib()

    def to_document(self):
        return {
            "to": self.to,
            "title": self.title,
            "body": self.body,
            "sender": self.sender,
        }
