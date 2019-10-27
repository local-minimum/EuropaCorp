from abc import ABC, abstractmethod
import imaplib
import poplib


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

    def get_messages(self, user, password, delete=True):
        self.server.user(user)
        self.server.pass_(password)
        n_messages = len(self.server.list()[1])

        for idx in range(n_messages):
            getter = self.server.retr(idx + 1)
            if next(getter) == b'+OK ':
                yield next(getter)
            else:
                # TODO: Handle NOK
                next(getter)

            # This is just how much data we just got
            next(getter)

        if delete:
            for idx in range(n_messages):
                self.server.dele(idx + 1)

        self.server.quit()


def get_server(domain, port):
    if port == 110:
        return MailServerPop(domain, port)
    return MailServerImap(domain, port)
