import os
from time import sleep
from pathlib import Path

import prometheus_client as prometheus
from pymongo import MongoClient
from pymongo.database import Database

from .controller import process_communications
from .storygateway import StoryGateway

MONGO_URI = os.environ.get("EUCO_MONGO_URI", "mongodb://mongodb")
MONGO_DB = os.environ.get("EUCO_MONGO_DB", "euco")
STORIES_PATH = os.environ.get("EUCO_STORIES_PATH", "/var/euco/stories")

FIFTEEN_MINUTES = 15 * 60

COMMUNICATIONS_COUNTER = prometheus.Counter(
    'gamemaker_communications_total',
    'Number of communications processed by Gamemaker',
    ['story_id', 'status', 'type']
)

STORYGATEWAY_ERRORCOUNTER = prometheus.Counter(
    'gamemaker_stories_total',
    'Number of communications processed by Gamemaker',
    ['story_id', 'status']
)


def get_db(uri: str, db: str) -> Database:
    mongo_client = MongoClient(uri)
    return mongo_client[db]


db = get_db(MONGO_URI, MONGO_DB)
storygateway = StoryGateway(Path(STORIES_PATH), STORYGATEWAY_ERRORCOUNTER)
prometheus.start_http_server(8000)

while True:
    process_communications(db, storygateway, COMMUNICATIONS_COUNTER)
    sleep(FIFTEEN_MINUTES)
