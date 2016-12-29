import json
from flask import Flask, request, current_app, render_template, redirect, url_for
from signinghub_api import SigningHubAPI

# Create a web application with Flask
app = Flask(__name__)

# Copy local_settings.py from local_settings_example.py
# Edit local_settings.py to reflect your CLIENT_ID and CLIENT_SECRET
app.config.from_pyfile('local_settings.py')    # Read example_app.local_settings.py

# Initialize the SigningHub API wrapper
signinghub_api = SigningHubAPI(
        app.config.get('SIGNINGHUB_CLIENT_ID'),
        app.config.get('SIGNINGHUB_CLIENT_SECRET'),
        app.config.get('SIGNINGHUB_USERNAME'),
        app.config.get('SIGNINGHUB_PASSWORD'),
        app.config.get('SIGNINGHUB_SCOPE')
        )

# Retrieve config settings from local_settings.py
signinghub_library_document_id = app.config.get('SIGNINGHUB_LIBRARY_DOCUMENT_ID')
signinghub_template_name = app.config.get('SIGNINGHUB_TEMPLATE_NAME')
recipient_user_name = app.config.get('RECIPIENT_USER_NAME')
recipient_user_email = app.config.get('RECIPIENT_USER_EMAIL')
recipient_field_name = app.config.get('RECIPIENT_FIELD_NAME')
recipient_field_value = app.config.get('RECIPIENT_FIELD_VALUE')

# Display the home page
@app.route('/')
def home_page():
    access_token = request.args.get('token')

    # Render the home page
    return render_template('home.html',
            access_token=access_token)


@app.route('/new_token')
def new_token():
    access_token = signinghub_api.get_access_token()

    # Show error message if needed
    if signinghub_api.last_error_message:
        return render_template('show_error_message.html',
                               access_token=access_token,
                               last_function_name=signinghub_api.last_function_name,
                               last_error_message=signinghub_api.last_error_message)
    # Redirect to home page
    return redirect(url_for('home_page')+'?token='+access_token)


# Retrieve and render a list of Adobe Sign Library Documents
@app.route('/show_packages')
def show_packages():
    # Get access token from the URL query string
    access_token = request.args.get('token')

    # signinghub_api.delete_package(access_token, 201080)

    # Use SigningHubAPI to retrieve a list of library documents
    if access_token:
        packages = signinghub_api.get_packages(access_token)
    else:
        packages = []

    for package in packages:
        print(json.dumps(package, indent=4))

    # Show error message if needed
    if signinghub_api.last_error_message:
        return render_template('show_error_message.html',
                               access_token=access_token,
                               last_function_name=signinghub_api.last_function_name,
                               last_error_message=signinghub_api.last_error_message)
    # Render the list of documents
    return render_template('show_packages.html',
                           access_token=access_token,
                           packages=packages)


# Create and render an Adobe Sign Widget
@app.route('/show_iframe')
def show_iframe():
    # Get access token from the URL query string
    access_token = request.args.get('token')
    if not access_token: return redirect('/')

    # Create a package
    package_name = '2017 Contract - '+recipient_user_name+' - '+recipient_user_email
    package_id = signinghub_api.add_package(access_token, package_name)

    # Add a document from the document library
    if package_id:
        document_id = signinghub_api.upload_document_from_library(access_token, package_id, signinghub_library_document_id)

        # Rename document
        if document_id:
            document_name = package_name
            success = signinghub_api.rename_document(access_token, package_id, document_id, document_name)

            # Add a template
            if success:
                template_name = 'ExampleAgreementTemplate'
                success = signinghub_api.apply_workflow_template(access_token, package_id, document_id, template_name)

            # print fields, so that we can determine the name of the text field
            if success:
                fields = signinghub_api.get_document_fields(access_token, package_id, document_id)
                print('Fields:', json.dumps(fields, indent=4))

                # Pre-fill the text field
                success = signinghub_api.update_textbox_field(access_token, package_id, document_id,
                        fields, recipient_field_name, recipient_field_value)

            # Add signer
            if success:
                success = signinghub_api.update_workflow_user(access_token, package_id, recipient_user_email, recipient_user_name)

            # Share Package
            if success:
                success = signinghub_api.share_document(access_token, package_id)

    # Show error message if needed
    if signinghub_api.last_error_message:
        return render_template('show_error_message.html',
                               access_token=access_token,
                               last_function_name=signinghub_api.last_function_name,
                               last_error_message=signinghub_api.last_error_message)

    # Render the IFrame with the document for signing
    return render_template('show_iframe.html',
                           access_token=access_token,
                           package_id=package_id,
                           user_email=recipient_user_email)


# SigningHub Callback, called after a user finishes the IFrame
@app.route('/signinghub/callback')    # Must match SigningHub's Application call-back URL setting
def signinghub_callback():
    # Retrieve callback info from the query parameters
    access_token = request.args.get('token')
    package_id = request.args.get('document_id')    # legacy parameter name. It really points to the Package.
    language_code = request.args.get('language')
    user_email = request.args.get('user_email')

    # Render a finished message
    return render_template('finished.html',
                           access_token=access_token,
                           package_id=package_id,
                           language_code=language_code,
                           user_email=user_email)

