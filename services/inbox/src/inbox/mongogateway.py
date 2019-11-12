import datetime as dt
from typing import Dict, Union

from pymongo.database import Database

MAILSCOLLECTION = 'mails'


def insert_mail(
    db: Database,
    mail: Dict[str, str],
):
    doc: Dict[str, Union[str, dt.datetime]] = {k: v for k, v in mail.items()}
    doc['created_time'] = dt.datetime.utcnow()
    doc['medium'] = 'mail'
    result = db[MAILSCOLLECTION].insert_one(doc)
    return str(result.inserted_id)
