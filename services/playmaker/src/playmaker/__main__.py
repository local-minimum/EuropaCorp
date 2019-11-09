import os
from time import sleep

import prometheus_client as prometheus
from pymongo import MongoClient
from pymongo.database import Database

MONGO_URI = os.environ.get("EUCO_MONGO_URI", "mongodb://mongodb")
MONGO_DB = os.environ.get("EUCO_MONGO_DB", "euco")

FIFTEEN_MINUTES = 15 * 60


def get_db(uri: str, db: str) -> Database:
    mongo_client = MongoClient(uri)
    return mongo_client[db]


db = get_db(MONGO_URI, MONGO_DB)
prometheus.start_http_server(8000)

while True:
    sleep(FIFTEEN_MINUTES)
