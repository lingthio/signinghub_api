"""
Copyright 2016, SolidBuilds.com. All rights reserved.
Author: Ling Thio, ling.thio@gmail.com
"""

from __future__ import print_function
import requests
import json

LOCAL_DEBUG = True                      # Print local debug info or not
API_BASE_URL = 'api/rest/v5/'


# The SigningHubAPI class offers access to the Adobe Sign REST API version 5
class SigningHubAPI(object):

    # Creates an instance of the SigningHubAPI class.
    # - client_id:     See Adobe Sign > API > API Applications > YOURAPP > Configure OAuth for Application
    # - client_secret: See Adobe Sign > API > API Applications > YOURAPP > Configure OAuth for Application
    def __init__(self, client_id='', client_secret='', username='', password='', scope=''):
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password
        self.scope = scope
        self.base_url = 'https://api.signinghub.com/v3/'
        self.last_function_name = None
        self.last_error_message = None
        pass


    # Returns the access_token on success.
    # Returns '' otherwise.
    def get_access_token(self):
        self.last_function_name = 'SigningHubAPI.get_access_token'
        access_token = ''
        if self.client_id and self.client_secret and self.username and self.password:
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json',
            }
            payload = {
                'grant_type': 'password',
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'username': self.username,
                'password': self.password,
            }

            # Call the SigningHub API
            url = 'https://api.signinghub.com/authenticate'
            response = requests.post(url, headers=headers, data=payload)

            # Process the response
            if response.status_code in (200, 201):
                data = response.json()
                access_token = data.get('access_token')
                self._print_success()
            else:
                self._print_response_error('POST', url, headers, payload, response)

        return access_token


    def add_package(self, access_token, package_name):
        self.last_function_name = 'SigningHubAPI.add_package'
        package_id = 0
        if access_token:
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': 'Bearer ' + access_token,
            }
            payload = {
                'package_name': package_name,
            }
            url = self.base_url + 'packages'
            response = requests.post(url, headers=headers, json=payload)

            # Process the response
            if response.status_code in (200, 201):
                json_data = response.json()
                package_id = json_data.get('package_id')
                self._print_success()
            else:
                self._print_response_error('GET', url, headers, payload, response)

        return package_id


    def upload_document_from_library(self, access_token, package_id, library_document_id):
        self.last_function_name = 'SigningHubAPI.upload_document_from_library'
        document_id = 0
        if access_token:
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': 'Bearer ' + access_token,
            }
            url = self.base_url + 'packages/' + str(package_id) + '/documents/library/' + str(library_document_id)
            response = requests.post(url, headers=headers)

            # Process the response
            if response.status_code in (200, 201):
                json_data = response.json()
                document_id = json_data.get('document_id')
                self._print_success()
            else:
                self._print_response_error('POST', url, headers, None, response)

        return document_id


    def rename_document(self, access_token, package_id, document_id, document_name):
        self.last_function_name = 'SigningHubAPI.last_function_name'
        success = False
        if access_token:
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': 'Bearer ' + access_token,
            }
            payload = {
                'document_name': document_name,
            }
            url = self.base_url + 'packages/' + str(package_id) + '/documents/' + str(document_id)
            response = requests.put(url, headers=headers, json=payload)

            # Process the response
            if response.status_code in (200, 201):
                success = True
                self._print_success()
            else:
                self._print_response_error('PUT', url, headers, payload, response)

        return success


    def apply_workflow_template(self, access_token, package_id, document_id, template_name):
        self.last_function_name = 'SigningHubAPI.apply_workflow_template'
        success = False
        if access_token:
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': 'Bearer ' + access_token,
            }
            payload = {
                'template_name': template_name,
                'apply_to_all': True,
            }
            url = self.base_url + 'packages/' + str(package_id) + '/documents/' + str(document_id) + '/template'
            response = requests.post(url, headers=headers, json=payload)

            # Process the response
            if response.status_code in (200, 201):
                success = True
                self._print_success()
            else:
                self._print_response_error('POST', url, headers, payload, response)

        return success


    def delete_package(self, access_token, package_id):
        self.last_function_name = 'SigningHubAPI.delete_package'
        if access_token:
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': 'Bearer ' + access_token,
            }
            url = self.base_url + 'packages/'+str(package_id)
            response = requests.delete(url, headers=headers)

            # Process the response
            if response.status_code in (200, 201):
                self._print_success()
            else:
                self._print_response_error('DELETE', url, headers, None, response)


    # Get a list of library documents.
    # Returns a list of library document information records on success.
    # Returns None otherwise.
    def get_packages(self, access_token, folder='INBOX'):
        self.last_function_name = 'SigningHubAPI.get_packages'
        packages = None

        # Retrieve a list of library documents
        if access_token:
            headers = {
                'Authorization': 'Bearer '+access_token,
                'Accept': 'application/json',
                'x-folder': folder,
                # 'x-search-text': '',
            }

            # Call the API
            url = self.base_url + 'packages/ALL/1/100'
            response = requests.get(url, headers=headers)

            # Process the response
            if response.status_code in (200, 201):
                response_body = response.json()
                packages = response_body
                self._print_success()
            else:
                self._print_response_error('GET', url, headers, None, response)

        return packages


    # Find a library document by document name.
    # Returns the library document ID on success.
    # Returns None otherwise.
    def find_package_by_name(self, packages, package_name):
        self.last_function_name = 'SigningHubAPI.find_package_by_name'
        package_id = None
        if packages:
            for package in packages:
                if package['package_name'] == package_name:
                    package_id = package['package_id']

        return package_id


    def update_workflow_user(self, access_token, package_id, user_email, user_name):
        self.last_function_name = 'SigningHubAPI.update_workflow_user'
        success = False
        if access_token:
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': 'Bearer ' + access_token,
            }
            payload = {
                'user_email': user_email,
                'user_name': user_name,
                'role': 'SIGNER',
                'email_notification': True,
            }
            url = self.base_url + 'packages/' + str(package_id) + '/workflow/1/user'
            response = requests.put(url, headers=headers, json=payload)

            # Process the response
            if response.status_code in (200, 201):
                success = True
                self._print_success()
            else:
                self._print_response_error('PUT', url, headers, payload, response)

        return success


    def get_document_fields(self, access_token, package_id, document_id):
        self.last_function_name = 'SigningHubAPI.get_document_fields'
        fields = None

        # Retrieve a list of documents fields
        if access_token:
            headers = {
                'Authorization': 'Bearer '+access_token,
                'Accept': 'application/json',
            }

            # Call the API
            url = self.base_url + 'packages/' + str(package_id) + '/documents/' + str(document_id) + '/fields'
            response = requests.get(url, headers=headers)

            # Process the response
            if response.status_code in (200, 201):
                response_body = response.json()
                fields = response_body
                self._print_success()
            else:
                self._print_response_error('GET', url, headers, None, response)

        return fields


    def update_textbox_field(self, access_token, package_id, document_id, field_name, field_value):
        self.last_function_name = 'SigningHubAPI.update_textbox_field'
        success = False
        if access_token:

            # Retrieve all fields
            fields = self.get_document_fields(access_token, package_id, document_id)

            # Find field by name
            old_field = None
            for field in fields['text']:
                if field['field_name']==field_name:
                    old_field = field

            if old_field:
                headers = {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'Authorization': 'Bearer ' + access_token,
                }
                payload = {
                    'field_name': field_name,
                    'page_no': old_field['page_no'],
                    'placeholder': old_field['placeholder'],
                    'value': field_value,
                    'max_length': old_field['max_length'],
                    'field_type': old_field['type'],
                    'validation_rule': old_field['validation_rule'],
                    'font': old_field['font'],
                    'dimensions': old_field['dimensions']['field'],
                }
                url = self.base_url + 'packages/' + str(package_id) + '/documents/' + str(document_id) + '/fields/text'
                response = requests.put(url, headers=headers, json=payload)

                # Process the response
                if response.status_code in (200, 201):
                    success = True
                    self._print_success()
                else:
                    self._print_response_error('PUT', url, headers, payload, response)

        return success


    def share_document(self, access_token, package_id):
        self.last_function_name = 'SigningHubAPI.share_document'
        success = False
        if access_token:
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': 'Bearer ' + access_token,
            }
            url = self.base_url + 'packages/' + str(package_id) + '/workflow'
            response = requests.post(url, headers=headers)

            # Process the respon
            # se
            if response.status_code in (200, 201):
                success = True
                self._print_success()
            else:
                self._print_response_error('POST', url, headers, None, response)

        return success


    def _print_success(self):
        self.last_error_message = None
        if LOCAL_DEBUG:
            print(self.last_function_name+'() completed successfully.')


    def _print_response_error(self, method, url, headers, payload, response):
        self.last_error_message = response.json().get('Message', 'Unknown error')
        if LOCAL_DEBUG:
            print(self.last_function_name+'() failed.')
            print(method, url)
            print('headers:', json.dumps(headers, indent=4))
            if payload:
                print('payload:', json.dumps(payload, indent=4))
            print('status_code:', response.status_code)
            print('error_message:', self.last_error_message)
