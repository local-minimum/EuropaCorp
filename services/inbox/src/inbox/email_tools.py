from email.message import Message
import email
from typing import Union, List, Dict
import re

from .exceptions import UnhandledEmailStructure


def get_mail_from_bytes(
    data: Union[List[bytes], bytes]
) -> Message:
    if isinstance(data, list):
        data = b'\n'.join(data)

    return email.message_from_bytes(data)


def mail_to_name(mail_str: str) -> str:
    if "." in mail_str:
        name = ' '.join([
            part.capitalize().strip() for part in mail_str.split('.')
        ])
    else:
        name = mail_str.strip()
    if '_' in name:
        name = ' '.join([
            part.capitalize().strip() for part in mail_str.split('_')
        ])
    return name


def get_name_from(from_str: str) -> str:
    match = re.match(r'[^<@]*', from_str)
    if match:
        name = mail_to_name(match.group())
    if not name:
        match = re.match(r'<([^@]*)', from_str)
        if match:
            name = mail_to_name(match.groups()[0]).capitalize()
        else:
            name = from_str
    return name


def get_mail_from(from_str: str) -> str:
    result = re.search(r'[^ <@]*@[^ >@]*\.[^ >@]{2,}', from_str)
    if result:
        return result.group()
    return from_str


def body_to_string(
    body: Union[List[Message], str, bytes, None],
) -> str:
    if isinstance(body, bytes):
        return body.decode()
    elif isinstance(body, str):
        return body
    raise UnhandledEmailStructure()


def get_data_object_from_mail(
    mail: Message
) -> Dict[str, str]:

    data = {
        'name': get_name_from(mail['From']),
        'mailer': get_mail_from(mail['From']),
        'reciever': get_mail_from(mail['To']),
        'body': '',
    }
    if mail.is_multipart():
        for part in mail.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get('Content-Disposition'))
            if ctype == 'text/plain' and 'attachment' not in cdispo:
                data['body'] = body_to_string(mail.get_payload(decode=True))
                break
    else:
        data['body'] = body_to_string(mail.get_payload(decode=True))
    return data
