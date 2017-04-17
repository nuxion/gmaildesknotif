from __future__ import print_function
import ipdb
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

class Gmail:
    def __init__(self):
        credentials = get_credentials()
        self.http = credentials.authorize(httplib2.Http())
        # Creo el servicio a usar, en este caso gmail
        self.service = discovery.build('gmail', 'v1', http=self.http)
        self.newMails = []
        self.oldMails = loadFile()
        
    def listMails(self, maxResults=10):
        """ Atraves del api de google obtengo los 10 ultimos mensajes 
        del INBOX. 
        Genera la lista self.newMails() con el id de todos los mails nuevos."""
        
        # Api specific
        response = self.service.users().messages().list(userId='me', labelIds='INBOX', maxResults=maxResults).execute()
        #ipdb.set_trace()
        # Si hay mensajes en la respuesta, arma la lista.
        if 'messages' in response:
            #messages = []
            # 'messages' es una lista que viene la respuesta json de la llamada al api
            #messages.extend(response['messages'])
            for m in response['messages']:
                self.newMails.append(m['id'])
    def compareMsgs(self):
        temp3 = [x for x in self.oldMails if x not in self.newMails]
        print (temp3)
    def save(self):
        saveFile(self.newMails, pathSTR="lastids.txt")
        
        
def loadFile(pathSTR="lastids.txt"):
    listIDS=[]
    with open (pathSTR, "r") as fileids:
        for line in fileids:
            # se ejecuta rstrip() para remover el '\n'
            listIDS.append(line.rstrip())
            #ipdb.set_trace()
    return listIDS 
def saveFile(savedata, pathSTR="newids.txt"):
    """ Method that recive a listvalue and write it to the file. 
    `savedata` []
    `pathSTR` string. """
    with open (pathSTR, "w") as filewrite:
        for x in savedata:
            filewrite.write(x+"\n")
        #filewrite(savedata)
        
    
if __name__ == "__main__":
    listaMails = Gmail()
    listaMails.listMails()
    listaMails.compareMsgs()
    listaMails.save() 
    
    #listaMails.saveNewMsgs()
