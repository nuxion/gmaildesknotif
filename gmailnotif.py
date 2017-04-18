#!/usr/bin/env python3
from __future__ import print_function
import ipdb
import httplib2
import os
import time

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import json
import subprocess
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
@profile
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
    @profile
    def __init__(self):
        
        # Initializaation of the gmail api
        credentials = get_credentials()
        self.http = credentials.authorize(httplib2.Http())
        # Creo el servicio a usar, en este caso gmail
        self.service = discovery.build('gmail', 'v1', http=self.http)
        # Inicializaciones propias de la clase
        self.newMails = []
        self.oldMails = loadFile()
    @profile    
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
    @profile
    def mailbymail(self, listIDS):
        listMails = []
        for m in listIDS:
            #ipdb.set_trace()
            response = self.service.users().messages().get(userId='me', id=m, fields="payload/headers").execute()
            dictEmail = {}
            for e in response['payload']['headers']:
                if e['name'] == 'Date':
                    dictEmail['date'] = e['value']
                elif e['name'] == 'From':
                    dictEmail['from'] = e['value']
                elif e['name'] == 'Subject':
                    dictEmail['subject'] = e['value']
            listMails.append(dictEmail)
        return listMails
                
    @profile    
    def compareMsgs(self):
        """ Verify the oldMails with the newMails, and return only the unique element. """
        #temp3 = [x for x in self.oldMails if x not in self.newMails]
        temp3 = [x for x in self.newMails if x not in self.oldMails]
        return temp3 
    @profile
    def saveNew(self):
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
def sendNotifications(allData):
    #cmd = "/home/nuxion/scripts/notify.sh"
    cmd = "/usr/bin/notify-send -u critical"
    for d in allData:
        strMsg = "\"" + "F:" + d['from'] + "\n" + "S:" + d['subject'] + "\""
        command = cmd + " " + strMsg
        # Not take params
        #subprocess.Popen([cmd, "-u normal", strMsg], stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        subprocess.Popen([command], shell=True)
    
if __name__ == "__main__":
    while True:
        listaMails = Gmail()
        listaMails.listMails()
        newElements = listaMails.compareMsgs()
        # if i have new mails then
        if newElements:
            # Save the new list of messages
            listaMails.saveNew() 
            allData=listaMails.mailbymail(newElements)
            #ipdb.set_trace()
            sendNotifications(allData) 
        #del listaMails
        #del newElements
        time.sleep(30)
        
        
              
        
