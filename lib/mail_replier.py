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
    def __init__(self):
        pass

    def create_message(self, original_message, message_text):
      headers = {}
      for header in original_message['payload']['headers']:
          headers[header['name']] = header['value']

      message = MIMEText(message_text)
      message['To'] = headers['From']
      message['From'] = 'me'
      message['Subject'] = 'Re: %s' % headers['Subject']
      message['ThreadId'] = original_message['threadId']
      message['References'] = headers['Message-ID']
      message['In-Reply-To'] = headers['Message-ID']
      raw = base64.urlsafe_b64encode(message.as_string())
      mail = base64.urlsafe_b64decode(raw.encode('ASCII'))
      return {'raw': raw}

    def reply_message(self, service, user_id, original_message, new_text):
      try:
          content_part = original_message['payload']['parts'][0]
          content_part_as_text = base64.urlsafe_b64decode(content_part['body']['data'].encode('ASCII'))

          is_german = detect(content_part_as_text) == 'de'
          new_text = self.response_contents(is_german)

          body = self.create_message(original_message, new_text)
          message = (service.users().messages()
                                    .send(userId=user_id,
                                            body=body)
                                            .execute())
      except errors.HttpError, error:
          print 'An error occurred: %s' % error

    def response_contents(self, is_german):
        file = 'content/de.txt' if is_german else 'content/en.txt'
        with open(file, 'r') as reponse_content:
            data = reponse_content.read()
            return data
