import base64

class MailRetriever:
    def __init__(self, service):
        self.service = service

    def retrieve_emails(self, user_id='me', query='is:unread label:test'):
        self.user_id = user_id
        self.query = query
        response = self.service.users().messages() \
                                       .list(userId=user_id,
                                             q=query).execute()
        messages = []
        if 'messages' in response:
            messages.extend(self.get_messages(response))

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = self.service.users().messages() \
                                           .list(userId=user_id,
                                                 q=query,
                                                 pageToken=page_token).execute()
            messages.append(self.get_messages(response))
        return messages

    def get_messages(self, response):
        message_ids = response['messages']
        messages = []
        for message_id in message_ids:
            message_content = self.get_message_content(message_id)
            messages.append(message_content)
        return messages

    def get_message_content(self, message_id):
        return self.service.users().messages() \
                                   .get(userId=self.user_id,
                                        id=message_id['id'],
                                        format='full').execute()
