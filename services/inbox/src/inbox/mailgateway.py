from abc import ABC, abstractmethod
import imaplib
import poplib

from .email_tools import get_data_object_from_mail, get_mail_from_bytes


class MailServer(ABC):
    @abstractmethod
    def __init__(self, domain, port):
        pass

    @abstractmethod
    def get_messages(self, user, password, delete=True):
        pass


class MailServerImap(MailServer):
    def __init__(self, domain, port):
        self.server = imaplib.IMAP4(domain, port)

    def get_messages(self, user, password, delete=True):
        with self.server as connection:
            connection.login(user, password)

            # Go to INBOX
            connection.select()

            # Return all messages
            _, inboxmsgs = connection.search(None, 'ALL')
            for num in inboxmsgs[0].split():
                yield connection.fetch(num, '(RFC822)')

            # Delete all deleted mails
            if delete:
                for num in inboxmsgs[0].split():
                    connection.store(num, '+FLAGS', '\\Deleted')
                connection.expunge()


class MailServerPop(MailServer):
    def __init__(self, domain, port):
        self.server = poplib.POP3(domain, port)
        self._tls = False

    def get_messages(self, user, password, delete=True):
        if self._tls:
            self.server.stls()
        self.server.user(user)
        self.server.pass_(password)
        n_messages = len(self.server.list()[1])

        for idx in range(n_messages):
            response = self.server.retr(idx + 1)
            status, bytes, size = response
            if status == b'+OK ':
                mail = get_mail_from_bytes(bytes)
                #TODO: prometheus log recieved OK mail
                yield get_data_object_from_mail(mail)
            else:
                #TODO: prometheus log recieved FAILED mail
                pass

        if delete:
            for idx in range(n_messages):
                self.server.dele(idx + 1)

        self.server.quit()

    def use_tls(self):
        self._tls = True


def get_server(domain, port):
    if port in [110, 995]:
        server = MailServerPop(domain, port)
        if port == 995:
            server.use_tls()
        return server
    return MailServerImap(domain, port)
