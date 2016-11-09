import base64
import mimetypes
import os

from apiclient import errors
from email.mime.text import MIMEText

# Language detect, make it deterministic
from langdetect import detect, DetectorFactory
DetectorFactory.seed = 0

class MailReplier:
    """ Object responsible for replying on all the given messages.
    """
    def __init__(self):
        pass

    def reply_message(self, service, original_message):
      """ Reply on the message given in either German or English, based on the
      original message.

      Keyword arguments:
          service -- Service object as provided by the Google login.
          original_message -- Needed to respond as a reply to the correct user.
      """
      email_data = original_message['payload']['parts'][0]['body']['data']
      email_data_as_text = base64.urlsafe_b64decode(email_data.encode('ASCII'))

      is_german = detect(email_data_as_text) == 'de'
      new_text = self._response_contents(is_german)

      body = self._create_message(original_message, new_text)
      service.users().messages()\
                     .send(userId='me', body=body)\
                     .execute()

    def _create_message(self, original_message, message_text):
        """ Create a message conform the Google API message format with the text
        given.

        Keyword arguments:
            original message -- The original message in Google API format.
            message_text     -- The new text as string.

        Returns:
            An encoded message ready to be send using the Gmail API.
        """
        headers = {}
        for header in original_message['payload']['headers']:
            headers[header['name']] = header['value']

        # Send to, and from the correct emailaddress
        message = MIMEText(message_text)
        message['To'] = headers['From']
        message['From'] = 'me'
        message['Subject'] = 'Re: %s' % headers['Subject']

        # Make sure the message send is a reply including the original message
        message['ThreadId'] = original_message['threadId']
        message['References'] = headers['Message-ID']
        message['In-Reply-To'] = headers['Message-ID']

        return {'raw': base64.urlsafe_b64encode(message.as_string())}

    def _response_contents(self, is_german):
        """ Return the text the reply should contain in either German or English
        based on the original message.

        Keyword arguments:
            is_german -- Boolean to determine if the respond should be German.

        Returns:
            The text to be used in the response as a plain String.
        """
        filename = '../content/de.txt' if is_german else '../content/en.txt'
        file = os.path.join(os.path.dirname(__file__), filename)
        with open(file, 'r') as reponse_content:
            return reponse_content.read()
