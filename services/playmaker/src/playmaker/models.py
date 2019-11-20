from typing import Dict, Any, Callable, Optional, List

import attr
from pymongo.cursor import Cursor

from .exceptions import StoryParsingError


class Rule:
    def __call__(self, bundle: "Communication") -> float:
        raise NotImplementedError()


@attr.s
class Link:
    story_id = attr.ib()
    execute_threshold = attr.ib()
    rule = attr.ib()

    @classmethod
    def from_data(
        cls,
        data: List[Dict[str, Any]],
        rule_builder: Callable[[Optional[Dict[str, Any]]], Rule],
    ) -> List["Link"]:
        def make_link(item) -> Link:
            try:
                story_id = item['story']
                execute_threshold = item['threshold']
            except (TypeError, KeyError):
                raise StoryParsingError("Could not parse link to {}".format(item.get('story', "NO STORY!")))
            return Link(
                story_id=story_id,
                rule=rule_builder(item.get('rule')),
                execute_threshold=execute_threshold,
            )

        return [make_link(item) for item in data]


@attr.s
class Story:
    title = attr.ib()
    sender = attr.ib()
    body = attr.ib()
    links = attr.ib()

    @classmethod
    def from_data(
        cls,
        data: Dict[str, Any],
        rule_builder: Callable[[Optional[Dict[str, Any]]], Rule],
    ) -> "Story":

        try:
            title = data['title']
            sender = data['sender']
            body = data['body']
            links = data['links']
        except KeyError:
            raise StoryParsingError("Malformatted story yml")
        return Story(
            title=title,
            sender=sender,
            body=body,
            links=Link.from_data(links, rule_builder),
        )


@attr.s
class Profile:
    mailer = attr.ib()
    mongodb_id = attr.ib(default=None)
    name = attr.ib(default=None)

    @classmethod
    def from_document(cls, doc: Cursor) -> "Profile":
        return cls(
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
