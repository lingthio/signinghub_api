# Authentication information
SIGNINGHUB_CLIENT_ID = 'ExampleApp'                     # Must match SigningHub's Application Name
SIGNINGHUB_CLIENT_SECRET = "Must match SigningHub's generated API Key"
SIGNINGHUB_USERNAME = 'yourname@example.com'            # Your SigningHub username
SIGNINGHUB_PASSWORD = 'yourpassword'                    # Your SigningHub password
SIGNINGHUB_SCOPE = SIGNINGHUB_USERNAME                  # Authorization scope

# Document information
SIGNINGHUB_LIBRARY_DOCUMENT_ID = 1234                   # Must match the ID of a SigningHub Library Document
SIGNINGHUB_TEMPLATE_NAME = 'ExampleContractTemplate'    # Must match the name of a SigningHub Template

# Information about the Recipient that signs the document
RECIPIENT_USER_NAME = 'Your Name'
RECIPIENT_USER_EMAIL = 'yourname@example.com'
RECIPIENT_FIELD_NAME = 'SH_FF_TEXT_314'                 # Must match the field name in a SigningHub Template
RECIPIENT_FIELD_VALUE = 'Some text field value'
