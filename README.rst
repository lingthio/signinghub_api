Synopsis
========

This is code example illustrates the use of the SiningHub API.

See http://manuals.ascertia.com/SigningHub-apiguide/default.aspx


Motivation
==========

I found that the API calls are well documented, but being new to this API,
I struggled trying to figure out which API calls to make and in what sequence.
I'm sharing this code example to provide a code illustration to other developers.

Though this code example is in Python (using the Flask application framework),
it still illustrates the API for developers in other programming languages.


Code organization
=================
* ``signinghub_api`` contains a simple wrapper for the SigningHub API.
* ``example_app`` contains a simple Flask application that calls the wrapper.
* ``runserver.py`` starts a development web server that serves the Flask application.


Installation
============
It is assumed that you have virtualenv and virtualenvwrapper installed and configured::

    # Clone this repository
    mkdir ~/dev
    git clone git@github.com:lingthio/signinghub_api.git signinghub_api

    # Create a virtualenv
    mkvirtualenv signinghub_api -p path/to/python
    cd signinghub_api
    pip install -r requirements.txt


Configuration
=============
Configure Signing Hub

- Create an account at signinghub.com
- Dashboard > Enterprise Actions > API Key
- Add (Blue plus sign)

  - Application Name: ExampleApp                             # This is your SIGNINGHUB_CLIENT_ID
  - Call-back URL: http://localhost:5000/signinghub/callback # Example app must serve this URL
  - Default Authentication Method: SigningHub ID
  - Generate the API Key                                     # This is your SIGNINGHUB_CLIENT_SECRET

Add a SigningHub Library Document

- Dashboard > Quick Action > Templates
- Under ``My Settings``, click on ``Library``
- Add a Library Document (blue plus sign)
- Upload a document (You can use ``example_app/ExampleAgreement.docx``)
- Click ``SAVE``
- Make note of the Library Document ID (shows up in the document list, after you click ``SAVE``)

Add a SigningHub Template

- Dashboard > Quick Action > Templates
- Add a Template (blue plus sign)
- Upload a document (You can use ``example_app/ExampleAgreement.docx``)
- Add a Placeholder Recipient (name and email will be pre-filled later)
- Click ``Next`` (top right)
- From the right sidebar, you can drag-and-drop form fields.

  - Drag-and-drop one Text field
  - Drag-and-drop one Electronic Signature field
  - Drag-and-drop one Date field

- Click on ``Done`` (top right)
- Make a note of the Template name

Configure the example web application::

    cd ~/dev/signinghub_api/example_app
    mv local_settings_example.py local_settings.py

Edit the local_settings.py
- Change the example settings to reflect your SigningHub account, document and template settings
- ``SIGNINGHUB_CLIENT_ID`` must reflect the Application name created in the previous section.
- ``SIGNINGHUB_CLIENT_SECRET`` must reflect the Application API Key created in the previous section.
- ``SIGNINGHUB_TEMPLATE_NAME`` must reflect the Template name created in the previous section.
- ``SIGNINGHUB_LIBRARY_DOCUMENT_ID`` must reflect the Library Document ID created in the previous section.
- ``SIGNINGHUB_TEMPLATE_NAME`` must reflect the Template name created in the previous section.


Starting the web application
============================
::

    workon signinghub_api
    cd ~/dev/signinghub_api
    python runserver.py

You can now point your browser to: http://localhost:5000/


Contributors
============
Ling Thio - ling.thio AT gmail.com
