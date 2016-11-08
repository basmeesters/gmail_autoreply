# Local
from google_authenticater import GoogleAuthenticater
from mail_retriever import MailRetriever
from mail_replier import MailReplier

# Scheduling
from threading import Thread
from time import sleep
from datetime import date, timedelta

class Main:
    """ Main object which used all the other classes to retrieve mail, send
    replies in either German or English, and does so in the given interval.
    """
    def __init__(self):
        """ Initialize the object. It creates all the components once so they
        can be reused in the scheduler.
        """
        google_authenticater = GoogleAuthenticater()
        self.service = google_authenticater.get_service()

        self.has_run = False
        self.mail_retriever = MailRetriever(self.service)
        self.mail_replier = MailReplier()

        thread = Thread(target=self._repeat_every_n_seconds, args=(2,))
        thread.start()

    def _start_all_services(self):
        """ Start the retrieving of emails, make sure only the newest ones are
        retrieved, and reply them automatically.
        """
        # It seems gmail only allows for dates and not for datetime to retrieve
        # new messages.
        today = date.today()
        yesterday = today - timedelta(1)

        query = 'is:unread label:overig'
        if self.has_run:
            query += " after:{1}".format(today.strftime('%Y/%m/%d'),
                                        yesterday.strftime('%Y/%m/%d'))
        messages = self.mail_retriever.retrieve_emails('me', query)

        # self.has_run = True
        for message in messages:
            self.mail_replier.reply_message(self.service, 'me', message)

    # Function with the timer
    def _repeat_every_n_seconds(self, seconds):
        print 'Iterate..'
        sleep(seconds)
        self._start_all_services()
        self._repeat_every_n_seconds(seconds)

if __name__ == '__main__':
    Main()
