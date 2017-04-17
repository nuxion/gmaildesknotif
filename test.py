import subprocess
cmd = "notify-send"
strMsg="Prueba unitaria\n" + "\n" + str("tres")
print (strMsg)
subprocess.Popen([cmd, "-u normal", strMsg], shell=True)
cmd = cmd + " -u normal" + " " + strMsg
subprocess.Popen([cmd], shell=True)
