import pytest
from email.message import Message

from inbox import email_tools


@pytest.fixture
def raw_mail():
    return [
        b'From: Foo Bar <user@example.com>',
        b'To: <someone_else@example.com>',
        b'Subject: Test message',
        b'',
        b'Body would go here',
    ]


def test_get_mail_from_bytes(raw_mail):
    assert isinstance(email_tools.get_mail_from_bytes(raw_mail), Message)


def test_get_data_object_from_mail(raw_mail):
    mail = email_tools.get_mail_from_bytes(raw_mail)
    assert email_tools.get_data_object_from_mail(mail) == {
        'from': 'Foo Bar <user@example.com>',
        'to': '<someone_else@example.com>',
        'body': 'Body would go here',
    }
