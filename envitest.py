import os

if os.environ['http_proxy']:
    print (os.environ['http_proxy'])
else:
    print ("No se seteo variable")
