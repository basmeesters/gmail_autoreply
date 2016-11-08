import base64

class MailRetriever:
    """ Object responsible for retrieving emails from the user

    There is only one public method which returns the emails which were not
    retrieved before based on the query given
    """
    def __init__(self, service):
        self.service = service
        self.messages_retrieved_before = {}

    def retrieve_emails(self, user_id, query):
        """ Retrieve the emails of the user based on the query and messages
        already retrieved before

        Keyword arguments:
            user_id -- The gmail id of the user. 'me' can be used as default
            query   -- Query on which to filter messages

        Returns:
            List of messages (see Gmail API for format)
        """
        self.user_id = user_id
        self.query = query
        response = self.service.users().messages() \
                                       .list(userId=user_id,
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
        return messages

    def _get_messages_on_page(self, response):
        """ Get the message ids & their contents on the retrieved page
        Keyword arguments:
            response -- Parsed json response from the API call
        Returns:
            All message contents for the response given
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
                                   .get(userId=self.user_id,
                                        id=message_id['id'],
                                        format='full').execute()
