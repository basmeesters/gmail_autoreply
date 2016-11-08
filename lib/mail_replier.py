import base64
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
import os
from apiclient import errors

# Language detect, make it deterministic
from langdetect import detect, detect_langs, DetectorFactory
DetectorFactory.seed = 0

class MailReplier:
    """ Object responsible for relpying on all the given messages.
    """
    def __init__(self):
        pass

    def reply_message(self, service, user_id, original_message):
      """ Reply on the message given in either German or English, based on the
      original message.
      """
      try:
          email_data = original_message['payload']['parts'][0]['body']['data']
          email_data_as_text = base64.urlsafe_b64decode(email_data
                                                            .encode('ASCII'))

          is_german = detect(email_data_as_text) == 'de'
          new_text = self._response_contents(is_german)

          body = self._create_message(original_message, new_text)
        #   service.users().messages()\
        #                  .send(userId=user_id, body=body)
        #                  .execute()
      except errors.HttpError, error:
          print 'An error occurred: %s' % error

    def _create_message(self, original_message, message_text):
        """ Create a message conform the Google API message format with the text
        given.

        Keyword arguments:
            original message -- The original message in Google API format
            message_text     -- The new text as string
        """
        headers = {}
        for header in original_message['payload']['headers']:
            headers[header['name']] = header['value']

        message = MIMEText(message_text)
        message['To'] = headers['From']
        message['From'] = 'me'
        message['Subject'] = 'Re: %s' % headers['Subject']

        # The code below should make sure the message send is a reply, but for
        # unknown reasons yet it doesn't include the original message
        message['ThreadId'] = original_message['threadId']
        message['References'] = headers['Message-ID']
        message['In-Reply-To'] = headers['Message-ID']

        # mail = base64.urlsafe_b64decode(raw.encode('ASCII'))
        return {'raw': base64.urlsafe_b64encode(message.as_string())}

    def _response_contents(self, is_german):
        """ Return the text the reply should contain in either German or English
        based on the original message.
        """
        file = 'content/de.txt' if is_german else 'content/en.txt'
        with open(file, 'r') as reponse_content:
            data = reponse_content.read()
            return data
