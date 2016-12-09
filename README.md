SaaS Company assignments
========================

Introduction
------------
When you start the program it will start retrieving messages from myInbox. It is
now configured to retrieve the messages from my 'overig' folder. I used this as
a dedicated folder to test my program. It polls now every two seconds. Both the
time and query to search for can be changed in main.py.

After it retrieves messages it will create a reply for each of them. It checks
if it can detect it as German, and if so send a response in German. Otherwise
it will respond in English. When retrieving again it will only get messages
received today (as we know that we have everything before that). And will check
if there are any new messages in those and respond again. The terminal will
provide information about what it is doing and how many new messages are
retrieved.

Setup
-----
1. Install python packages
  * Setuptools
  * GoogleAPI
  * Langdetect
  * Nosetests

2. [Get google API access](https://developers.google.com/gmail/api/quickstart/python?hl=nl)

    Note that the program is now configured to work on one machine. To make it
    work on other machines a new client_secret file and Google account are
    probably needed. Go through the steps in the link & replace the
    client_secret.json to make it work.

3. Start the program by navigating to the root of the project and execute:

  `python -B lib/main.py`

  The program will print output to the terminal to show how it is progressing.

4. Test the program by navigating to the root of the project and execute:

  `nosetests`

  However, note that some tests will not pass based on the account from which
  the tests are run. See possible improvements for more details.

Structure
---------
All the functionality of the application is present in the directory lib. It
contains four packages. Each package contains a class - which may be a bit
overkill for such a small program - but it will be easier to extend in the
future.

The packages:
* google_authenticater provides a class to authenticate your machine to use the
  Google API. It returns a service object which can be used to make calls.
* mail_retriever provides a class which retrieves the mails based on the query
  it is given. It keeps track of which messages were seen before so to not
  parse & respond to them again.
* mail_replier provides a class which expects original messages and
  automatically answers them in German or English based on the files found in
  the content directory. The messages are now standard templates I could find.
* main creates all the classes and uses them to periodically execute all the
  actions necessary to retrieve & reply automatically.

Possible improvements
---------------------
* A start was made to use command line arguments (see main.py) but because the
  Google authentication also used the command line arguments this interfered and
  gave errors. It would be nice if both could work without interfering with each
  other.
* The program nows runs forever and needs to be forcefully stopped. When it
  starts again it does not remember on which emails it already replied. The
  dictionary used could be written to a file and read again to avoid this.
* There is a bug which makes sure that if you reply to yourself you do not see
  the response in a thread. This fortunately does not happen when you get mail
  from other senders.
* The tests are mostly related to my account and not all will pass on other
  machines / accounts. Since it is quite a lot of work to setup all mock-ups I
  decided to set it out of scope for this assignment.
* I decided to not test the google_authenticater & main as that would require a
  lot of mock-ups as well.
