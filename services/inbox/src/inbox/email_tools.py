import email
from typing import Union, List, Dict


def get_mail_from_bytes(
    data: Union[List[bytes], bytes]
) -> email.message.Message:
    if isinstance(data, list):
        data = b'\n'.join(data)

    return email.message_from_bytes(data)


def get_data_object_from_mail(
    mail: email.message.Message
) -> Dict[str, str]:
    data = {
        'from': mail['From'],
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
