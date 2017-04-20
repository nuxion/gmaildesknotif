#!/bin/bash

# VARIABLES
# In crontab with 'notify-send' its neccesary set a Display 
export DISPLAY=:0
BASEDIR="/home/nuxion/Projects/gmail/gmail"
MAILDIR=$BASEDIR"/mails/"
notify="/usr/bin/notify-send"
PYTH="/usr/bin/python2.7"
urgency='critical'
nameapp="Gmail Notification v0.03"
var=0
# MENU 
while [ "$1" != "" ]; do
    case $1 in
        -p | --proxy )           shift
                                http_proxy=$1
                                ;;
        -a | --all-notifs )    var=1
                                ;;
        #-u | --urgency )       urgency=$2
        #                        ;;
        -h | --help )           usage
                                exit
                                ;;
        * )                     echo "error"
                                exit 1
    esac
    shift
done
export http_proxy
echo $http_proxy # debug
### MAIN ### 
# Chequeo todas las condiciones
# Si no existe lastids.txt lo crea, en base a este archivo
# main.py comparara con los nuevos mails obtenidos. 
if [ ! -f $BASEDIR/lastids.txt ]; then
    echo "123456" > $BASEDIR/lastids.txt
else
    # por el momento para evitar temas de paths relativos y demas
    # ejecuto main.py desde su path  
    #cd $BASEDIR && $PYTH main.py
    # posible bug, si o si debe recibir una variable, 
    # por mas que este vacia
    cd $BASEDIR && env http_proxy=$http_proxy $PYTH envitest.py
    echo "ejecuta script"
fi

# Una vez ejecutado el script, 
# verifico si hay files creados en el directorio de mails.
if [ "$(ls -A $MAILDIR)" ]; then
	# para decidir si muestro todos los mails en una sola notificacion
	if [ $var -eq 1 ];then
        # mail.txt tiene todos los mails en un solo archivo 
        # en vez de un txt por cada uno
        # por como escapa caractares xfce4-notifyd es necesario
        # escapar manualmente algunos caracteres
		sed -i 's/<//g' $MAILDIR/mail.txt && sed -i 's/>//g' $MAILDIR/mail.txt
		$notify -u $urgency "Gmail Notification v0.03" "$( cat $MAILDIR/mail.txt)"
	else
        # sino imprimo una notificacion distinta por c/mail
		for x in `ls $MAILDIR | grep -v mail.txt`
		do
			sed -i 's/<//g' $MAILDIR$x && sed -i 's/>//g' $MAILDIR$x  
			$notify -u $urgency  "Gmail Notification v0.03" "$(cat $MAILDIR$x)"
		done
	fi
	# only for debug purposes
    #cp $MAILDIR/*.txt /home/nuxion/scripts/gmaildesknotif/mails2
    # borro los mails, ya que funcionan como flag para detectar si
    # es necesario enviar las notifs
	#rm $MAILDIR/*.txt
else 
    # for debug purposes
	echo "No hay mails nuevos"
fi
