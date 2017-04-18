"""
Modulo que tiene todo los metodos relacionados a trabajar con archivos.

"""
import os
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

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

def saveFile(savedata, pathSTR="newids.txt"):
    """ Method that recive a listvalue and write it to the file. 
    `savedata` []
    `pathSTR` string. """
    with open (pathSTR, "w") as filewrite:
        for x in savedata:
            filewrite.write(x+"\n")
        #filewrite(savedata)
        
def loadFile(pathSTR="lastids.txt"):
    listIDS=[]
    with open (pathSTR, "r") as fileids:
        for line in fileids:
            # se ejecuta rstrip() para remover el '\n'
            listIDS.append(line.rstrip())
            #ipdb.set_trace()
    return listIDS        

def saveDict(saveDict, pathSTR="mails/"):
    listToMail = []
    i = 0
    for mail in saveDict:
        strMail = mail['from'] + "\n" + mail['subject']
        listToMail.append(strMail) 
        listToMail.append("----------")
        with open (pathSTR + str(i) + ".txt", "w") as filemail:
            filemail.write(strMail)
        i = i + 1
    saveFile(listToMail, "mails/mail.txt")
