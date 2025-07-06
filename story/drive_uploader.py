from __future__ import print_function
import os
import pickle
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/drive.file']
FOLDER_NAME = "IG Stories"

def authenticate_drive():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(host='localhost', port=7860)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)
    return service

def get_or_create_folder(service, folder_name):
    
    response = service.files().list(
        q=f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false",
        spaces='drive',
        fields='files(id, name)',
    ).execute()

    files = response.get('files', [])
    if files:
        folder_id = files[0]['id']
        print(f"[Drive] 📁 Found folder '{folder_name}' (ID: {folder_id})")
        return folder_id

    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }

    folder = service.files().create(
        body=file_metadata,
        fields='id'
    ).execute()

    folder_id = folder.get('id')
    print(f"[Drive] 📁 Created folder '{folder_name}' (ID: {folder_id})")
    return folder_id

def upload_to_drive(image_path, order_id, customer_name):
    service = authenticate_drive()
    folder_id = get_or_create_folder(service, FOLDER_NAME)

    file_metadata = {
        'name': f"{order_id}_{customer_name}.jpg",
        'parents': [folder_id],
        'mimeType': 'image/jpeg'
    }

    media = MediaFileUpload(image_path, mimetype='image/jpeg')

    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id, webViewLink'
    ).execute()

    print(f"[Drive] ✅ Uploaded to '{FOLDER_NAME}': {file_metadata['name']} (ID: {file['id']})")
    print(f"[Drive] 🔗 View link: {file.get('webViewLink')}")
    return file.get('webViewLink')
