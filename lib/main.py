# Taken from Quickstart Gmail API and modified to suit our needs
from __future__ import print_function
import base64
import email
import html2text

from login import Login

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from langdetect import detect

def get_flags():
  try:
    import argparse
    return argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
  except ImportError:
    return None

def main():
    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    login = Login()
    service = discovery.build('gmail', 'v1', http = login.get_http(get_flags()))

    response = service.users().messages().list(userId='me',
                                               q='is:unread label:overig').execute()

    if 'messages' in response:
      message_ids = response['messages']
      for message_id in message_ids:
          message = service.users().messages().get(userId='me', id=message_id['id'], format='full').execute()
        #   msg_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))
        #   mime_msg = email.message_from_string(msg_str)
          part = message['payload']['parts'][0]
          msg_str = base64.urlsafe_b64decode(part['body']['data'].encode('ASCII'))
          print(detect(msg_str))

    while 'nextPageToken' in response:
      page_token = response['nextPageToken']
      response = service.users().messages().list(userId='is:unread', q='is:unread label:overig',
                                         pageToken=page_token).execute()
      messages.extend(response['messages'])

if __name__ == '__main__':
    main()
