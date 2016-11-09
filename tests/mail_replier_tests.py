import unittest
import base64
import os

from google_authenticater import GoogleAuthenticater
from mail_retriever import MailRetriever
from mail_replier import MailReplier

class MailReplierTests(unittest.TestCase):
    def setUp(self):
        google_authenticater = GoogleAuthenticater()
        self.service = google_authenticater.get_service()
        self.mail_retriever = MailRetriever(self.service)
        self.mail_replier = MailReplier()

    # Test if the message contains the correct attributes and text
    def test_create_message(self):
        messages = self.mail_retriever.retrieve_emails(None)
        self.assertTrue(len(messages) > 0)
        first_message = messages[0]
        raw_message = self.mail_replier \
                              ._create_message(first_message, 'TEST TEXT')
        encoded_message = raw_message['raw'].encode('ASCII')
        decoded_message = base64.urlsafe_b64decode(encoded_message)
        self.assertIn('TEST TEXT', decoded_message)
        self.assertIn('From: me', decoded_message)
        self.assertIn('Subject: Re:', decoded_message)

    def test_reply_in_german(self):
        text = self.mail_replier._response_contents(True)
        file = os.path.join(os.path.dirname(__file__), '../content/de.txt')
        with open(file, 'r') as reponse_content:
            data = reponse_content.read()
            self.assertIn(data, text)

    def test_reply_in_english(self):
        text = self.mail_replier._response_contents(False)
        file = os.path.join(os.path.dirname(__file__), '../content/en.txt')
        with open(file, 'r') as reponse_content:
            data = reponse_content.read()
            self.assertIn(data, text)

    # Test that the amount of emails has gone up after auto-replying myself
    def test_reply_message(self):
        # Get all unread email amount in the inbox today
        self.mail_retriever.has_run = True
        query = self.mail_retriever._set_query('from:(meesters.bas@gmail.com)')
        old_messages = self.mail_retriever.retrieve_emails(query)
        amount_unread_old = len(old_messages)

        # Need to make a new retriever as the old one already keeps track of
        # which unread messages we have already seen
        self.mail_retriever = MailRetriever(self.service)
        self.mail_retriever.has_run = True

        first_message = old_messages[0]
        self.mail_replier.reply_message(self.service, first_message)
        new_messages = self.mail_retriever.retrieve_emails(query)
        amount_unread_new = len(new_messages)

        self.assertEqual(amount_unread_new, amount_unread_old + 1)
