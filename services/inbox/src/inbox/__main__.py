import os
from time import sleep

import prometheus_client as prometheus
from pymongo import MongoClient
from pymongo.database import Database

from .mailgateway import get_server
from .mongogateway import insert_mail

HOST = os.environ.get("EUCO_MAIL_SERVER_HOST", "")  # Defaults to localhost
PORT = int(os.environ.get("EUCO_MAIL_SERVER_PORT", 143))
USER = os.environ.get("EUCO_MAIL_USER", "noone")
PASSWORD = os.environ.get("EUCO_MAIL_PWD", "nopwd")
MONGO_URI = os.environ.get("EUCO_MONGO_URI", "mongodb://mongodb")
MONGO_DB = os.environ.get("EUCO_MONGO_DB", "euco")
HALF_HOUR = 30 * 60

MAIL_COUNTER = prometheus.Counter(
    'inbox_mails_processed',
    'Number of mails received.'
)

def get_db(uri: str, db: str) -> Database:
    mongo_client = MongoClient(uri)
    return mongo_client[db]


def process_mails(
    host: str, port: int, user: str, password: str, db: Database,
):
    server = get_server(host, port)
    for mail in server.get_messages(user, password):
        insert_mail(db, mail)
        MAIL_COUNTER.inc()


if __name__ == '__main__':
    db = get_db(MONGO_URI, MONGO_DB)
    prometheus.start_http_server(8000)
    while True:
        process_mails(HOST, PORT, USER, PASSWORD, db)
        sleep(HALF_HOUR)
