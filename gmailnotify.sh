#!/bin/bash
export DISPLAY=:0
BASEDIR="/home/nuxion/scripts/gmaildesknotif"
MAILDIR=$BASEDIR"/mails/"

var=$1
notify="/usr/bin/notify-send"
PYTH="/usr/bin/python3"
# check_ok() 
# Chequeo todas las condiciones
	
	if [ ! -f $BASEDIR/lastids.txt ]; then
		echo "123456" > $BASEDIR/lastids.txt
	else
		cd $BASEDIR && $PYTH main.py
	fi
	if [ $# -eq 0 ]; then
		var=0
	fi

### MAIN ### 
if [ "$(ls -A $MAILDIR)" ]; then
	
	if [ $var -eq 1 ];then
		$notify -u critical "Gmail Notification v0.02" "$( cat $MAILDIR/mail.txt)"
	else
		for x in `ls $MAILDIR | grep -v mail.txt`
		do
			$notify -u critical "Gmail Notification v0.02" "$(cat $MAILDIR$x)"
		done
	fi
	#rm $MAILDIR/*.txt
else 
	echo "No hay mails nuevos"
fi
