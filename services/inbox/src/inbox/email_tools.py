import email

def get_mail_from_bytes(bytes):
    if isinstance(bytes, list):
        bytes = b'\n'.join(bytes)

    parser = email.feedparser.BytesFeedParser()
    parser.feed(bytes)
    return parser.close()


def get_data_object_from_mail(mail):
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
    return data
