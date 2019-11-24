#!/usr/bin/env python3
from typing import Optional
from pathlib import Path
from unittest.mock import Mock

from .playmaker.storygateway import StoryGateway
from .playmaker.models import Communication, Profile
from .playmaker.game import compose_response, get_next_storyid_and_profile

gw = StoryGateway(Path('./playmaker/stories'), Mock())
name = None
sender = None
profile = None

story_id: Optional[str] = input("Story ID (empty for default start story): ")
while True:
    if not story_id:
        story_id = None

    story = gw.get_story(story_id)
    if not story:
        exit(1)

    if name is None:
        print("\n== Your Profile ==")
        sender = input("MAIL: ")
        name = input("NAME: ")
        profile = Profile(mailer=sender, name=name)

    response = compose_response(sender, story, profile)
    if response is None:
        print("!!! NO MAIL CREATED")
        exit(2)

    print("\n== EuCo Mail ==")
    print("FROM: {}".format(response.sender))
    print("TO: {}".format(response.to))
    print("TITLE: {}".format(response.title))
    print("BODY:\n{}\n\n".format(response.body))

    while True:
        print("\n== Your response ==")
        reciever = input("TO: ")
        title = input("TITLE: ")
        body_parts = []
        prev_line = None
        while True:
            body_line = input("BODY (multiline):")
            if not body_line and not prev_line:
                break
            prev_line = body_line
            body_parts.append(body_line)
        body = "\n".join(body_parts)

        comm = Communication(
            mongodb_id=None,
            mailer=sender,
            name=name,
            reciever=reciever,
            body=body,
            medium="mail",
        )

        next_storyid, profile = get_next_storyid_and_profile(
            [comm], story, profile,
        )
        if next_storyid is None:
            print("!! No valid link found")
        else:
            story_id = next_storyid
            break
