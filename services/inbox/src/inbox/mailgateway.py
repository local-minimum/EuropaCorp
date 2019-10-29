from abc import ABC, abstractmethod
import imaplib
import poplib
from typing import Iterator, Dict

from .email_tools import get_data_object_from_mail, get_mail_from_bytes


class MailServer(ABC):
    @abstractmethod
    def __init__(self, domain: str, port: int):
        pass

    @abstractmethod
    def get_messages(
        self, user: str, password: str, delete: bool = True
    ) -> Iterator[Dict[str, str]]:
        pass


class MailServerImap(MailServer):
    def __init__(self, domain: str, port: int):
        self.server = imaplib.IMAP4(domain, port)

    def get_messages(
        self, user: str, password: str, delete: bool = True,
    ) -> Iterator[Dict[str, str]]:
        self.server.login(user, password)

        # Go to INBOX
        self.server.select()

        # Return all messages
        _, inboxmsgs = self.server.search(None, 'ALL')
        for num in inboxmsgs[0].split():
            _, data = self.server.fetch(num, '(RFC822)')
            mail = get_mail_from_bytes(data)
            # TODO: prometheus log recieved OK mail
            yield get_data_object_from_mail(mail)

        # Delete all deleted mails
        if delete:
            for num in inboxmsgs[0].split():
                self.server.store(num, '+FLAGS', '\\Deleted')
            self.server.expunge()
        self.server.close()
        self.server.logout()


class MailServerPop(MailServer):
    def __init__(self, domain: str, port: int):
        self.server = poplib.POP3(domain, port)
        self._tls = False

    def get_messages(
        self, user: str, password: str, delete: bool = True,
    ) -> Iterator[Dict[str, str]]:
        if self._tls:
            self.server.stls()
        self.server.user(user)
        self.server.pass_(password)
        n_messages = len(self.server.list()[1])

        for idx in range(n_messages):
            response = self.server.retr(idx + 1)
            status, data, size = response
            if status == b'+OK ':
                mail = get_mail_from_bytes(data)
                # TODO: prometheus log recieved OK mail
                yield get_data_object_from_mail(mail)
            else:
                # TODO: prometheus log recieved FAILED mail
                pass

        if delete:
            for idx in range(n_messages):
                self.server.dele(idx + 1)

        self.server.quit()

    def use_tls(self):
        self._tls = True


def get_server(domain: str, port: int) -> MailServer:
    if port in [110, 995]:
        server = MailServerPop(domain, port)
        if port == 995:
            server.use_tls()
        return server
    return MailServerImap(domain, port)
