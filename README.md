SaaS company assignments
========================

Setup
-----
1. Install pip
2. Install python packages
  * Setuptools
  * GoogleAPI
  * Langdetect
3. Get google API access


Structure
---------
All the functionality of the application is present in the directory lib. It
contains four packages.
* google_authenticater provides a class to authenticate your machine to use the
  Google API. It returns a service object which can be used to make calls.
* mail_retriever provides a class which retrieves the mails based on the query
  it is given. It keeps track of which messages were seen before so to not
  parse & respond to them again.
* mail_replier provides a class which expects original messages and
  automatically answers them in German or English based on the files found in
  the content directory.
* main creates all the classes and uses them to periodically execute all the
  actions necessary to retrieve & reply automatically.
