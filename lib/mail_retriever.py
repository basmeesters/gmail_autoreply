import base64
from datetime import date, timedelta

class MailRetriever:
    """ Object responsible for retrieving emails from the user.

    There is only one public method which returns the emails which were not
    retrieved before based on the query given.
    """
    def __init__(self, service):
        self.service = service
        self.messages_retrieved_before = {}
        self.has_run = False

    def retrieve_emails(self, query):
        """ Retrieve the emails of the user based on the query and messages
        already retrieved before.

        Keyword arguments:
            query -- Query on which to filter messages.

        Returns:
            List of messages (see Gmail API for format).
        """
        query = self._set_query(query)
        response = self.service.users().messages() \
                                       .list(userId='me',
                                             q=query).execute()
        # For each page get the messages and append them to the result
        messages = []
        if 'messages' in response:
            messages.extend(self._get_messages_on_page(response))

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = self.service.users().messages() \
                                           .list(userId=user_id,
                                                 q=query,
                                                 pageToken=page_token).execute()
            messages.append(self._get_messages_on_page(response))
        self.has_run = True
        print 'Got %s new messages' % len(messages)
        return messages

    def _set_query(self, query):
        """ Set the query to either the default or the one given as argument.

        A default argument would not help here as None would override it. It
        also updates the query once it knows it has retrieved email before to
        only look at emails received today.

        Keyword arguments:
            query -- Query to search for in the Gmail inbox as a plain String.

        Returns:
            The query possible default or updated to search for messages
            retrieved today.
        """
        query = 'is:unread label:overig' if not query else query
        if self.has_run:
            # It seems gmail only allows for dates and not for datetime to
            # retrieve new messages.
            today = date.today()
            yesterday = today - timedelta(1)
            query += " after:{1}".format(today.strftime('%Y/%m/%d'),
                                         yesterday.strftime('%Y/%m/%d'))
        print 'Used the following query to find messages: %s' % query
        return query

    def _get_messages_on_page(self, response):
        """ Get the message ids & their contents on the retrieved page.

        Keyword arguments:
            response -- Parsed json response from the API call.

        Returns:
            All message contents for the response given.
        """
        message_ids = response['messages']
        messages = []
        for message_id in message_ids:
            if not message_id['id'] in self.messages_retrieved_before:
                message_content = self._get_message_content(message_id)
                messages.append(message_content)

                # The value is not important, just if the key exists
                self.messages_retrieved_before[message_id['id']] = True
        return messages

    def _get_message_content(self, message_id):
        """ Get the actual content of messages such as sender, subject, etc.
        
        Keyword arguments:
            message_id -- Make an API call based on the message id

        Returns:
            A message according to the Google message format
        """
        return self.service.users().messages() \
                                   .get(userId='me',
                                        id=message_id['id'],
                                        format='full').execute()
