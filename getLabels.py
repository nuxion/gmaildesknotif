from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import json
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    #results = service.users().messages.list(userId='me').execute()
    response = service.users().labels().list(userId='me').execute()
    labels = response['labels']
    for label in labels:
      print ('Label id: %s - Label name: %s' % (label['id'], label['name']))
    #return labels
def listMails():
    # Firts part of authentication
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    
    # Creo el servicio a usar, en este caso gmail
    service = discovery.build('gmail', 'v1', http=http)
    # Hago la llamada especifica al api:
    response = service.users().messages().list(userId='me', labelIds='INBOX', maxResults=10).execute()
    print (response)
    # Obtengo una lista de Ids y ThreadsId
    # En response que es un json, existe el vector 'messages'
    messages = []
    if 'messages' in response:
        messages.extend(response['messages'])
    
    # Recorro cada mensaje para buscar las properties que me interesan.
    for m in messages:
        with open ("lastids.txt", "a") as fileids:
                       fileids.write(m['id']+"\n")
        #print(m['id'])
        response2 = service.users().messages().get(userId='me', id=m['id'], fields="payload/headers").execute()
        #print (json.dumps(response2, sort_keys=True, indent=4))
        """print("Date: " + response2['payload']['headers'][10]['value'])
        print("Subject: " + response2['payload']['headers'][12]['value'])
        print("From: " + response2['payload']['headers'][16]['value'])
        print("--------")"""
        for e in response2['payload']['headers']:
            #print (e)
            #print ("------")
            if e['name'] == 'Date':
                print ("Date: " + e['value'])
            elif e['name'] == 'From':
                print ("From: " + e['value'])
            elif e['name'] == 'Subject':
                 print ("Subject: " + e['value'])
            
        print ("----")

    #while 'nextPageToken' in response:
    #  page_token = response['nextPageToken']
    #  response = service.users().messages().list(userId='me', pageToken=page_token).execute()
    #  messages.extend(response['messages'])
    
if __name__ == '__main__':
    main()
    listMails()
