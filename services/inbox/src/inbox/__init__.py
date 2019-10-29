import os
from .mailgateway import get_server

host = os.environ.get("EUCO_MAIL_SERVER_HOST", "")  # Defaults to localhost
port = int(os.environ.get("EUCO_MAIL_SERVER_PORT", 143))
user = os.environ.get("EUCO_MAIL_USER", "noone")
password = os.environ.get("EUCO_MAIL_PWD", "nopwd")


def process_mails(host: str, port: int, user: str, password: str):
    server = get_server(host, port)
    for mail in server.get_messages(user, password):
        print(mail)
        print("---")


if __name__ == '__main__':
    process_mails(host, port, user, password)
