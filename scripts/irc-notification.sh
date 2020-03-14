#!/bin/bash
state="${SERVICESTATE:-$HOSTSTATE}";
laststate="${LASTSERVICESTATE:-$LASTHOSTSTATE}";

colourstate () {
	# default to red
	statecolour=04
	if [ "$1" == "UP" ] || [ "$1" == "OK" ]
	then
		statecolour="03"
	fi
	if [ "$1" == "WARNING" ]
	then
		statecolour="08"
	fi
	echo "\x03$statecolour$1\x03"
}

colouredstate=$(colourstate $state)
colouredlaststate=$(colourstate $laststate)

# default to red
color="04"
if [ "$NOTIFICATIONTYPE" == "ACKNOWLEDGEMENT" ] || [ "$NOTIFICATIONTYPE" == "CUSTOM" ]
then
	color="02"
fi

if [ "$NOTIFICATIONTYPE" == "RECOVERY" ]
then
	color="03"
fi

colouredtype="\x03$color$NOTIFICATIONTYPE\x03"

prefix=""
middle=""
if [ "$NOTIFICATIONUMBER" -gt 1 ] && [ "$NOTIFICATIONTYPE" != "ACKNOWLEDGEMENT" ]
then
	if [ "$laststate" == "$state" ]
	then
		prefix="Reminder of "
		middle="still "
		suffix=" ($NOTIFICATIONUMBER reminders since $LONGDATETIME)"
	else
		middle="State change $colouredlaststate -> "
	fi
fi

if [ -z "$SERVICESTATE" ]
then
	alert="$HOSTNAME"
else
	alert="$HOSTNAME/$SERVICENAME"
fi

echo -e "[i2] $prefix$colouredtype - $alert $middle$colouredstate$suffix" | telnet bot.sown.org.uk 4444
