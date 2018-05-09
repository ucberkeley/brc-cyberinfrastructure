# Google Drive API helper functions
# Many based on AdamAndersonFindSumerian.ipynb

import codecs
import httplib2
import os
import io
import sys
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.http import MediaFileUpload
from apiclient import discovery, errors
from oauth2client import client
from oauth2client import tools
from oauth2client import file

# Google Drive authentication based on AdamAndersonFindSumerian.ipynb

SCOPES = 'https://www.googleapis.com/auth/drive'
APPLICATION_NAME = 'gDriveConnect'

# Based on AdamAndersonFindSumerian.ipynb
# Reference: https://developers.google.com/drive/v3/web/quickstart/python
def get_credentials(CLIENT_SECRET_FILE):
    import argparse
    parser = argparse.ArgumentParser(parents=[tools.argparser])
    parser.add_argument('-f', help=argparse.SUPPRESS)

    flags = parser.parse_known_args()[0]
    flags.noauth_local_webserver = True
    
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.meh')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'gDriveConnect.json')
    store = file.Storage(credential_path)    
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store, flags)
        print('Storing credentials to ' + credential_path)
    return credentials

def get_service(client_secret):
    credentials = get_credentials(client_secret)
    http = credentials.authorize(httplib2.Http())
    return discovery.build('drive', 'v3', http=http)

def match_extension(extension):
    return lambda file: file['name'][-(len(extension) + 1):] == '.' + extension

class GDrive:
    def __init__(self, client_secret):
        self.service = get_service(client_secret)

    def list_files(self, folder_id, extension=None):
        response = self.service.files().list(
            q="'" + folder_id + "' in parents and trashed=false", 
            spaces='drive',
            fields='nextPageToken, files(id, name)',
            pageToken=None).execute()
        files = response['files']
        if extension:
            files = list(filter(match_extension(extension), files))
        return files

    # Source: https://developers.google.com/drive/v3/web/manage-downloads
    # Source: AdamAndersonFindSumerian.ipynb
    def download_file(self, file_id, destination=None):
        request = self.service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            try:
                status, done = downloader.next_chunk()
                sys.stdout.write('.')
            except errors.HttpError as error :
                print('An error occurred pulling the next chunk:', error)
                break
        fh.seek(0)
        contents = fh.getvalue()
        if destination:
            with open(destination, 'wb') as f2:
                f2.write(contents)
                f2.close()
        fh.close()
        return contents

    # Google Drive upload based on AdamAndersonFindSumerian.ipynb
    def upload_file(self, name, path, destination_folder=None):
        file_metadata = { 'name': name }
        if destination_folder:
            file_metadata['parents'] = [destination_folder]
        media = MediaFileUpload(path, mimetype='text/plain')
        file = self.service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        return file

    def move_file(self, file_id, new_folder, old_folder=None):
        return self.service.files().update(
            fileId=file_id,
            addParents=new_folder,
            removeParents=old_folder).execute()

    def read_local_file(self, file_path, encoding='latin-1'):
        contents = ''
        with open(file_path, encoding=encoding) as f:
            for line in f.readlines():
                contents += line
        return contents
