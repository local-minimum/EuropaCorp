import os
from time import sleep

import prometheus_client as prometheus
from pymongo import MongoClient
from pymongo.database import Database

from .controller import process_communication
from .storygateway import StoryGateway

MONGO_URI = os.environ.get("EUCO_MONGO_URI", "mongodb://mongodb")
MONGO_DB = os.environ.get("EUCO_MONGO_DB", "euco")
STORIES_PATH = os.environ.get("EUCO_STORIES_PATH", "/var/euco/stories")

FIFTEEN_MINUTES = 15 * 60


def get_db(uri: str, db: str) -> Database:
    mongo_client = MongoClient(uri)
    return mongo_client[db]


db = get_db(MONGO_URI, MONGO_DB)
storygateway = StoryGateway(STORIES_PATH)
prometheus.start_http_server(8000)

while True:
    process_communications(db, storygateway)
    sleep(FIFTEEN_MINUTES)
