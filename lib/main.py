# Gmail API
from apiclient import discovery
from oauth2client import client
from oauth2client import tools

# Local
from login import Login
from mail_retriever import MailRetriever
from mail_replier import MailReplier

def get_flags():
    try:
        import argparse
        return argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    except ImportError:
        return None

def main():
    login = Login()
    service = discovery.build('gmail', 'v1', http = login.get_http(get_flags()))
    mail_retriever = MailRetriever(service)
    messages = mail_retriever.retrieve_emails('me', 'is:unread label:overig')
    # print(messages[0])

    mail_replier = MailReplier()
    mail_replier.reply_message(service, 'me', messages[0], 'some tekst')

if __name__ == '__main__':
    main()
