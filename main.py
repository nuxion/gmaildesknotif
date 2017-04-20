from __future__ import print_function
import httplib2
from gmailnotif import Gmail
from files import saveDict, get_credentials
#try:
#    import argparse
#    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
#except ImportError:
#    flags = None


if __name__ == "__main__":
    # inicializo el api, y traigo los nuevos elementos
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    listaMails = Gmail(http)
    listaMails.listMails()
    newElements = listaMails.compareMsgs()
    # if i have new mails then
    if newElements:
        # Save the new list of messages
        listaMails.saveNew() 
        allData=listaMails.mailbymail(newElements)
        #ipdb.set_trace()
        #sendNotifications(allData) 
        # saveDict() guarda en la carpeta mails/ los nuevos encontrados
        saveDict(allData)
