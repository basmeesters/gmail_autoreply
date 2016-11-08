# Gmail API
from apiclient import discovery
from oauth2client import client
from oauth2client import tools

# Local
from login import Login
from mail_retriever import MailRetriever
from mail_replier import MailReplier

# Scheduler
from threading import Thread
from time import sleep
from datetime import date, timedelta

class Main:
    def __init__(self):
        login = Login()
        self.service = login.get_service()

        self.has_run = False
        self.mail_retriever = MailRetriever(self.service)
        self.mail_replier = MailReplier()

        thread = Thread(target=self.timer, args=(2,))
        thread.start()

    def start_scheduler(self):
        # It seems gmail only allows for dates and not for datetime to retrieve new
        # messages
        today = date.today()
        yesterday = today - timedelta(1)

        query = 'is:unread label:overig'
        if self.has_run:
            query += " after:{1}".format(today.strftime('%Y/%m/%d'),
                                        yesterday.strftime('%Y/%m/%d'))
        messages = self.mail_retriever.retrieve_emails('me', query)

        self.has_run = True
        for message in messages:
            self.mail_replier.reply_message(self.service, 'me', message)

    # Function with the timer
    def timer(self, seconds):
        print 'Iterate..'
        sleep(seconds)
        self.start_scheduler()
        self.timer(seconds)

if __name__ == '__main__':
    Main()
