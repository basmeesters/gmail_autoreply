import os
import httplib2

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

# If modifying these scopes, delete the previously saved credentials
# at ~/.credentials/gmail_authentication.json
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.send']
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Automatic Gmail reply'

class GoogleAuthenticater:
    """ Object which authenticates with the Gmail API

    Mostly taken from quickstart example of the Gmail API page and modified to
    our needs. It only got one public method: get_service
    """

    def get_service(self):
        """ Returns: an autenticated service object with which calls can be made
        """
        credentials = self._get_credentials()
        return discovery.build('gmail', 'v1',
                               http=credentials.authorize(httplib2.Http()))

    def _get_flags(self):
        """ Get the flags needed for Google authenticate
        """
        try:
            import argparse
            return argparse.ArgumentParser(parents=[tools.argparser])\
                           .parse_args()
        except ImportError:
            return None

    def _get_credentials(self):
        """ Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'gmail_authentication.json')

        store = Storage(credential_path)
        credentials = store.get()
        flags = self._get_flags()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials
