from __future__ import print_function
import httplib2
import subprocess 
from gmailnotif import Gmail
from files import saveDict, get_credentials
#try:
#    import argparse
#    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
#except ImportError:
#    flags = None

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
