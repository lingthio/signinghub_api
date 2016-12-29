Example Python inteface to the Adobe Sign REST API
==================================================

The purpose of this code repository is to be an additinal information source
for developers wanting to interface to the Adobe Sign REST API.

I struggled a bit to make this work, and I'm publishing this code to save
other developers from this struggle.

As such is is NOT meant to be a fully functioning package and it will likely NOT be maintained,
beyond adding example functionality submitted by various contributors.

Though it's in Python, it probably serves developers of other programming languages too.


Create and Configure an Adobe Sign API Application
--------------------------------------------------
- Login to Adobe Sign Development Center at https://secure.na1.echosign.com/
- Navigate to `API` > `Adobe Sign API` > `API Applications`.
- Add a new API Application by clicking on the 'plus sign' icon.
- Select this API Application
- Click on `Configure OAuth for Application`.
- Take note of `Client ID` and `Client Secret`.
- Add `https://localhost:5443/adobe_sign/oauth_redirect` to the `Redirect URI` field (IMPORTANT!).
- Enable the appropriate `Enabled Scopes`:

    - Enable `user_login` with modfier `self`.
    - Enable `widget_write` with modifier `account`.
    - Enable `library_read` with modifier `account`.

- Click `Save`.


Install this repository
-----------------------
::

    cd ~/dev
    git clone git@github.com:lingthio/adobe_sign.git adobe_sign
    cd ~/dev/adobe_sign

`adobe_sign/adobe_sign.py` contains the reusable function library.

`example_app/` contains a simple Flask Application to illustrate the use of the library.


Create a virtualenv
-------------------
It is assumed that you've properly installed and configured mkvirtualenv::

    mkvirtualenv adobe_sign
    workon adobe_sign
    cd ~/dev/adobe_sign
    pip install -r requirements.txt


Configure the example web application
-------------------------------------
To avoid exposing sensitive security information, local_settings.py is excluded from the code repository.
An example file is included for convenience::

    cd ~/dev/adobe_sign/example_app
    cp local_settings_example.py local_settings.py

Edit `local_settings.py` and make sure `CLIENT_ID` and `CLIENT_SECRET`
matches the information from Adobe Sign's API Application configuration.


Running the example web application
-----------------------------------
The Adobe Sign API requires that the authentication code request redirects to
a secure URL (HTTPS instead of HTTP). To avoid conflicts with existing ports,
we configured this HTTPS web application to run on port 5443.

Start the example web server::

    cd ~/dev/adobe_sign/example_app
    python runserver.py

Point your browser to::

    https://localhost:5443/

Note the `s` in `https` and the `:5443` port number instead of the usual `:5000`.

Access Tokens
-------------
Access Tokens are temporary tokens that are required to call the Adobe Sign API.

API calls are made in three steps:

1. Request an Authentication Code
2. Request an Access Token (using the Authentication Code)
3. Call the Adobe Sign API (using the Access Token)

1. Request an Authentication Code
---------------------------------
An Authentication Code request is made with an HTTPS call to::

    GET https://secure.na1.echosign.com/public/oauth
        ?response_type=code
        &client_id=...
        &redirect_uri=...                   # make sure to url-encode this
        &scope=...
        &state=...                          # any developer-supplied value

Adobe Sign authenticates the web application by offering the code through a redirect to
the pre-defined URL that points to your web server. In our case::

    https://localhost:5443/adobe_sign/oauth_redirect
        ?code=...
        &api_access_point=https://.../      # make sure to url-encode this
        &state=...                          # any developer-supplied value

The Authentication Code is returned in the query parameter `code`

Note: Adobe Sign uses dynamic servers to process API requests from certain users.
The user assigned 'Access Point' is returned in the `api_access_point` query parameter
and must be used the base for this user's API calls.

In our example, the oauth url is constructed in adobe_sign/adobe_sign.py; make_oauth_url().

The request is initiated in example_app/templates/home.html; first `<a ...>...</a>` link.

The processing of the redirect response is done in example_app/example_app.py; oauth_redirect().

See https://secure.na1.echosign.com/public/static/oauthDoc.jsp

2. Request an Access Token
--------------------------
An Access Token request is made with an HTTPS call to::

    GET {api_access_point}oauth/token
        ?grant_type=authorization_code
        &client_id=...
        &client_secret=...
        &redirect_uri=...                   # make sure to url-encode this
        &code=...                           # Authentication code from previous step

The temporary Access Token is returned in the JSON response::

    {
        "token_type": "Bearer",
        "access_token": "...",
            ...
    }

In our example, this is done in adobe_sign/adobe_sign.py; get_access_token().

See https://secure.na1.echosign.com/public/static/oauthDoc.jsp


3. Call the Adobe Sign API
--------------------------
Since Adobe Sign uses dynamic servers to serve their users, the Access Token must
first be used to retrieve the API Access Point of a specific user.

Call a fixed URL to get the dynamic API Access Point with Access-Token in the header::

    # with Access-Token: ... in the header:
    GET https://api.echosign.com/api/rest/v5/base_uris

The dynamic Access Point is returned in as a JSON object::

    {
        "api_access_point": "...",
            ...
    }

Call the desired API with Access-Token in the header::

    # with Access-Token: ... in the header:
    GET {api_access_point}api/rest/v5/libraryDocuments

In our example, this is done in adobe_sign/adobe_sign.py; get_api_access_point().

See https://secure.na1.echosign.com/public/docs/restapi/v5


About Creating Widgets
----------------------
Note: The transient document must include an email form field. If not, Adobe Sign will add an extra page
to the PDF with a signature and email field.

Note: The email address will be verified, unless email address verification has been disabled.
Go to https://secure.na1.echosign.com/ > Account > Account Settings > Signature Preferences >
Widget Email Verification (near the bottom of this page).


Troubleshooting
---------------
If you notice `ConnectionError: ('Connection aborted.', error(54, 'Connection reset by peer'))`
it's because the requests package in python2.7 does not use SNI in SSL connections.
Use Python3.x to fix this issue.

If the `Request new Access Token` link displays this error message::

    Unable to authorize access because the client configuration is invalid: invalid_request

You need to check the following:

- example_app/local_settings.py: CLIENT_ID is properly set
- example_app/local_settings.py: CLIENT_SECRET is properly set
- Your `Redirect URI` in API Application configuration in Adobe Sign includes `https://localhost:5443/adobe_sign/oauth_redirect`.


Limitations
-----------
`adobe_sign` is far from complete and may evolve over time -- hopefully with your contributions.

Currently supported methods are::

    make_oauth_url()
    get_access_token()
    create_transient_document()
    get_library_documents():
    find_library_document_by_name()
    create_widget():


Adding functionality
--------------------
If you need to use other Adobe Sign APIs, you can do so by sub-classing SigningHubAPI
and adding the additional methods::

    from adobe_sign import SigningHubAPI

    # Sub-class SigningHubAPI
    class MySigningHubAPI(SigningHubAPI):

        # Add new functionality
        def create_and_send_agreement(access_token, document_creation_info)
            agreement_id = None

            if access_token:
                payload = {
                    "document_creation_info": agreement_create_info
                }

                # Call the Adobe Sign API
                call_response = self.call_adobe_sign_api_post(access_token, 'widgets', payload)

                # Process the response
                if call_response:
                    agreement_id = call_response.get('agreementId')
                else:
                    print('SigningHubAPI.create_and_send_agreement() failed.')

            return agreement_id

     # Use new functionality
     adobe_sign = MySigningHubAPI(...)
        ...
     access_token = adobe_sign.get_access_token(...)
        ...
     agreement_id = adobe_sign.create_and_send_agreement(...)

Be sure to email us your additions so we can incorporate it into the next release.
Better still, fork our repository, include your addition and submit a pull request.


Contact Information
-------------------
Ling Thio - ling.thio AT gmail.com
