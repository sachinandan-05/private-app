import pickle
import os
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow


def Create_Service(token_file=None, client_secret=None):
    API_SERVICE_NAME = 'drive'
    API_VERSION = 'v3'

    cred = None
    working_dir = os.getcwd()

    if not token_file:
        token_file = fr'{working_dir}/Private/token_file/token_drive_v3.pickle'
    if not client_secret:
        client_secret = fr'{working_dir}/Private/token_file/client_secret.json'

    try:
        with open(token_file, 'rb') as token:
            cred = pickle.load(token)
    except Exception as e:
        print(f'Error loading token file: {e}')

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            SCOPES = ["https://www.googleapis.com/auth/drive"]
            flow = InstalledAppFlow.from_client_secrets_file(client_secret, SCOPES)
            cred = flow.run_local_server()

        with open(token_file, 'wb') as token:
            pickle.dump(cred, token)

    if not os.path.exists(client_secret):
        print(msg())
    try:
        google_service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        print(API_SERVICE_NAME, API_VERSION, 'Service Created Successfully .....!')
        return google_service
    except:
        print(API_SERVICE_NAME, API_VERSION, 'Failed To Create Service .....!')
        return None


def msg():
    text = """
    
------------------------------------------------------------------------------------------------------------
|                                                                                                          |
|       Client Secret File Does Not Exist,                                                                 |
|       Please Download From Google Cloud Platform and Save As client_secret.json at /Private/token_file/  |
|       Here Documentation: https://developers.google.com/drive/api/quickstart/python                      |
|                                                                                                          |
------------------------------------------------------------------------------------------------------------
    
    """

    return text


if __name__ == '__main__':
    working_dir = os.getcwd()
    token_file = fr'{working_dir}/token_file/token_drive_v3.pickle'
    client_secret = fr'{working_dir}/token_file/client_secret.json'

    if os.path.exists(client_secret):
        service = Create_Service(token_file, client_secret)
    else:
        print(msg())
