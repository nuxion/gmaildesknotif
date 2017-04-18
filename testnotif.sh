#!/bin/bash
export DISPLAY=:0
BASEDIR="/home/nuxion/scripts/gmaildesknotif"
MAILDIR=$BASEDIR"/mails2/"
export http_proxy="http://localhost:8080"
export https_proxy="https://localhost:8080"
var=$1
notify="/usr/bin/notify-send"
PYTH="/usr/bin/python2.7"
# check_ok() 
# Chequeo todas las condiciones
	
	if [ ! -f $BASEDIR/lastids.txt ]; then
		echo "123456" > $BASEDIR/lastids.txt
	else
		#cd $BASEDIR && $PYTH main.py
		echo "ejecuta script"
	fi
	if [ $# -eq 0 ]; then
		var=0
	fi

### MAIN ### 
if [ "$(ls -A $MAILDIR)" ]; then
	
	if [ $var -eq 1 ];then
		sed -i 's/<//g' $MAILDIR/mail.txt && sed -i 's/>//g' $MAILDIR/mail.txt
		$notify -u critical "Gmail Notification v0.02" "$( cat $MAILDIR/mail.txt)"
	else
		for x in `ls $MAILDIR | grep -v mail.txt`
		do
			echo "mail x mail"
			sed -i 's/<//g' $MAILDIR$x && sed -i 's/>//g' $MAILDIR$x  
			$notify -u critical "Gmail TESTING" "$(cat $MAILDIR$x)"
		done
	fi
	#rm $MAILDIR/*.txt
else 
	echo "No hay mails nuevos"
fi
