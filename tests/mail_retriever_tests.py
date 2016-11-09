import unittest
from google_authenticater import GoogleAuthenticater
from mail_retriever import MailRetriever
from datetime import date, timedelta

class MailRetrieverTests(unittest.TestCase):
    def setUp(self):
        google_authenticater = GoogleAuthenticater()
        service = google_authenticater.get_service()
        self.mail_retriever = MailRetriever(service)

    # Test that the query is the default one if none is given
    def test_default_query(self):
        query = self.mail_retriever._set_query(None)
        self.assertEqual('is:unread label:overig', query)

    # Test that a question query can be given and is used
    def test_custom_query(self):
        query_text = 'label:starred'
        query = self.mail_retriever._set_query(query_text)
        self.assertEqual(query_text, query)

    # Test that the messages searched for are only those of today if run before
    def test_has_run_query(self):
        self.mail_retriever.retrieve_emails(None)
        query = self.mail_retriever._set_query(None)
        yesterday = (date.today() - timedelta(1)).strftime('%Y/%m/%d')
        self.assertEqual('is:unread label:overig after:%s' % yesterday, query)
        
    # Tests that the amount of unread emails is correct
    def test_retrieve_messages(self):
        messages = self.mail_retriever.retrieve_emails(None)
        self.assertTrue(len(messages) == 3)

    # Test that there are no new emails after running again
    def test_has_run_messages(self):
        self.mail_retriever.retrieve_emails(None)
        messages = self.mail_retriever.retrieve_emails(None)
        self.assertTrue(len(messages) == 0)
