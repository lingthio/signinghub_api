import json
from flask import Flask, request, current_app, render_template, redirect, url_for
from signinghub_api import SigningHubAPI

# Create a web application with Flask
app = Flask(__name__)

# Copy local_settings.py from local_settings_example.py
# Edit local_settings.py to reflect your CLIENT_ID and CLIENT_SECRET
app.config.from_pyfile('local_settings.py')    # Read example_app.local_settings.py

signinghub_api = SigningHubAPI(     # Initialize the SigningHubAPI package
        app.config.get('SIGNINGHUB_CLIENT_ID'),
        app.config.get('SIGNINGHUB_CLIENT_SECRET'),
        app.config.get('SIGNINGHUB_USERNAME'),
        app.config.get('SIGNINGHUB_PASSWORD'),
        app.config.get('SIGNINGHUB_SCOPE')
        )


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

    # Redirect to home page
    return redirect(url_for('home_page')+'?token='+access_token)


# Adobe Sign will redirect to this URL (https://localhost:5443/signinghub_api/oauth_redirect)
# in response to an authorization request (https://secure.na1.echosign.com/public/oauth).
@app.route('/signinghub/callback')
def oauth_redirect():
    print('CALLBACK called')
    return redirect(url_for('home_page'))


# Retrieve and render a list of Adobe Sign Library Documents
@app.route('/show_packages')
def show_packages():
    # Get access token from the URL query string
    access_token = request.args.get('token')

    # signinghub_api.delete_package(access_token, 201030)

    # Use SigningHubAPI to retrieve a list of library documents
    if access_token:
        packages = signinghub_api.get_packages(access_token)
    else:
        packages = []

    for package in packages:
        print(json.dumps(package, indent=4))

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

    library_document_id = 2998  # ID of Example Document
    camper_name_field_name = 'SH_FF_TEXT_314'

    user_email = 'ling_thio@yahoo.com'
    user_name = 'Firstname Lastname'
    camper_name = 'Camper One'
    package_name = '2017 Contract - '+user_email+' - '+camper_name

    package_id = 0
    # # Find package by package name
    # packages = signinghub_api.get_packages(access_token)
    # package_id = signinghub_api.find_package_by_name(packages, package_name)

    # Create package if needed
    if not package_id:
        # Create a package
        package_id = signinghub_api.add_package(access_token, package_name)
        if not package_id: return redirect('/?token='+access_token)

        # Add a document from the document library
        document_id = signinghub_api.upload_document_from_library(access_token, package_id, library_document_id)
        if not document_id:
            signinghub_api.delete_package(access_token, package_id)
            return redirect('/?token='+access_token)

        # Rename document
        signinghub_api.rename_document(access_token, package_id, document_id, package_name)

        # Add a template
        template_name = 'ExampleAgreementTemplate'
        signinghub_api.apply_workflow_template(access_token, package_id, document_id, template_name)

        fields = signinghub_api.get_document_fields(access_token, package_id, document_id)
        print('Fields:', json.dumps(fields, indent=4))

        # Pre-fill the camper name field
        signinghub_api.update_textbox_field(access_token, package_id, document_id, camper_name_field_name, camper_name)

        # Add signer
        signinghub_api.update_workflow_user(access_token, package_id, user_email, user_name)

        # Share Package
        if package_id:
            signinghub_api.share_document(access_token, package_id)

    # Render the IFrame with the document for signing
    return render_template('show_iframe.html',
            access_token=access_token,
            package_id=package_id,
            user_email=user_email)



