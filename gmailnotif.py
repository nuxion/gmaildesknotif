#!/usr/bin/env python3
from apiclient import discovery
from files import loadFile, saveFile, get_credentials

class Gmail:
    """ Clase principal que hace la llamada a la api de gmail
    y obtiene los ultimos 10 mails del INBOX. Los compara con la ultima lista obtenida y sacando la diferencia entre nuevos y viejos identifica si hay alertas. """
    
    def __init__(self, http):
        # Creo el servicio a usar, en este caso gmail
        self.service = discovery.build('gmail', 'v1', http=http)
        # Inicializaciones propias de la clase
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
                
    def compareMsgs(self):
        """ Verify the oldMails with the newMails, and return only the unique element. """
        #temp3 = [x for x in self.oldMails if x not in self.newMails]
        temp3 = [x for x in self.newMails if x not in self.oldMails]
        return temp3 
    def saveNew(self):
        saveFile(self.newMails, pathSTR="lastids.txt")
        
def sendNotifications(allData):
    """ Method to send notifications from the python process itself,
    DEPRECATED. """

    import subprocess 
    cmd = "/usr/bin/notify-send -u critical"
    for d in allData:
        strMsg = "\"" + "F:" + d['from'] + "\n" + "S:" + d['subject'] + "\""
        command = cmd + " " + strMsg
        # Not take params
        #subprocess.Popen([cmd, "-u normal", strMsg], stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        subprocess.Popen([command], shell=True)
   
    
if __name__ == "__main__":
    import time
    import httplib2
    credentials = get_credentials()
    pi = httplib2.proxy_info_from_url('http://localhost:8080')
    http = credentials.authorize(httplib2.Http(proxy_info=pi))
    while True:
        listaMails = Gmail(http)
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
        
              
        
