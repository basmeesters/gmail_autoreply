# Deal with command line arguments
import sys, getopt

# Scheduling
from threading import Thread
from time import sleep
from datetime import date, timedelta

# Local
from google_authenticater import GoogleAuthenticater
from mail_retriever import MailRetriever
from mail_replier import MailReplier

class Main:
    """ Main object which used all the other classes to retrieve mail, send
    replies in either German or English, and does so in the given interval.
    """
    def __init__(self, argv):
        """ Initialize the object. It creates all the components once so they
        can be reused in the scheduler.

        Keyword arguments:
            argv -- Command line arguments, not used anymore
        """
        google_authenticater = GoogleAuthenticater()
        self.service = google_authenticater.get_service()

        self.has_run = False
        self.mail_retriever = MailRetriever(self.service)
        self.mail_replier = MailReplier()

        # Change these to change the polling interval and query to search for
        self.query = None
        timeout = float(2,)

        thread = Thread(target=self._repeat_every_n_seconds(timeout))
        thread.start()

    def _start_all_services(self):
        """ Start the retrieving of emails, make sure only the newest ones are
        retrieved, and reply them automatically.
        """
        try:
            messages = self.mail_retriever.retrieve_emails(self.query)
            for message in messages:
                self.mail_replier.reply_message(self.service, message)
        except errors.HttpError, error:
            print 'An error occurred: %s' % error

    def _repeat_every_n_seconds(self, timeout):
        print 'Start retrieving every %s seconds' % timeout
        sleep(timeout)
        self._start_all_services()

        print 'Done reading & replying\n'
        self._repeat_every_n_seconds(timeout)


    # Not used because it interfers with google authentication..
    def _get_command_line_arguments(self, argv):
        try:
            opts, args = getopt.getopt(argv,"hq:t:",[])
        except getopt.GetoptError:
            print 'Program was called faulty, try lib/main.py -h'
            sys.exit(2)

        commands = {}
        for opt, arg in opts:
            if opt == '-h':
                print 'start the program with:\n'
                print '   lib/main.py -q <search query> -t <timeout in seconds>'
                print '\nExample:\n\n'\
                      '   lib/main.py -q \'is:unread label:test\' -t 300\n\n'\
                      'to autoreply on unread messages in the folder test '\
                      'every 5 minutes (300 s)'
                sys.exit()
            elif opt == '-q':
                commands['q'] = arg
            elif opt == '-t':
                commands['t'] = arg
        return commands

if __name__ == '__main__':
    Main(sys.argv[1:])
