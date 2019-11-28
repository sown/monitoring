#!/bin/bash
state="${SERVICESTATE:-$HOSTSTATE}";

color="04"
if [ "$state" == "UP" ] || [ "$state" == "OK" ]
then
	color="03"
fi
if [ "$NOTIFICATIONTYPE" == "ACKNOWLEDGEMENT" ] || [ "$NOTIFICATIONTYPE" == "CUSTOM" ]
then
	color="02"
fi

colouredstate="\x03$color$state\x03"
colouredtype="\x03$color$NOTIFICATIONTYPE\x03"

prefix=""
middle=""
if [ "$NOTIFICATIONUMBER" -gt 1 ] && [ "$NOTIFICATIONTYPE" != "ACKNOWLEDGEMENT" ]
then
	prefix="Reminder of "
	middle="still "
	suffix=" ($NOTIFICATIONUMBER reminders since $LONGDATETIME)"
fi

if [ -z "$SERVICESTATE" ]
then
	alert="$HOSTNAME is"
else
	alert="$HOSTNAME/$SERVICENAME"
fi

echo -e "[i2] $prefix$colouredtype - $alert $middle$colouredstate$suffix" | telnet bot.sown.org.uk 4444
