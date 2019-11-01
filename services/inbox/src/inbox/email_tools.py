from email.message import Message
import email
from typing import Union, List, Dict
import re


def get_mail_from_bytes(
    data: Union[List[bytes], bytes]
) -> Message:
    if isinstance(data, list):
        data = b'\n'.join(data)

    return email.message_from_bytes(data)


def get_name_from(from_str: bytes) -> str:
    match = re.match('[^<@]*', from_str)
    if match:
        if "." in match.group():
            name = ' '.join([
                part.capitalize().strip() for part in match.group().split('.')
            ])
        else:
            name = match.group().strip()
        if '_' in name:
            name = ' '.join([
                part.capitalize().strip() for part in match.group().split('_')
            ])
    else:
        name = from_str.encode()
    return name


def get_data_object_from_mail(
    mail: Message
) -> Dict[str, str]:

    data = {
        'from': mail['From'],
        'name': get_name_from(mail['From']),
        'to': mail['To'],
        'body': '',
    }
    if mail.is_multipart():
        for part in mail.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get('Content-Disposition'))
            if ctype == 'text/plain' and 'attachment' not in cdispo:
                data['body'] = part.get_payload(decode=True)
                break
    else:
        data['body'] = mail.get_payload(decode=True)
    if isinstance(data['body'], bytes):
        data['body'] = data['body'].decode()
    return data
