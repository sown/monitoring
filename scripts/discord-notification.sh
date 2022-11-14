#!/bin/bash

DIR=$(dirname "${BASH_SOURCE[0]}")
. $DIR/discord-notification-creds

state="${SERVICESTATE:-$HOSTSTATE}";
laststate="${LASTSERVICESTATE:-$LASTHOSTSTATE}";

type="$NOTIFICATIONTYPE"

prefix=""
middle=""
if [ "$NOTIFICATIONUMBER" -gt 1 ] && [ "$NOTIFICATIONTYPE" != "ACKNOWLEDGEMENT" ]
then
	if [ "$laststate" == "$state" ]
	then
		prefix="Reminder of "
		middle="still "
		suffix=" ($NOTIFICATIONUMBER reminders since $(date -d @$LONGDATETIME))"
	else
		middle="State change $laststate -> "
	fi
fi

if [ -z "$SERVICESTATE" ]
then
	alert="$HOSTNAME"
else
	alert="$HOSTNAME/$SERVICENAME"
fi

line="$prefix$type - $alert $middle$state$suffix"

curl -d "username=Icinga 2" -d "content=$line" "https://discord.com/api/webhooks/$discord_webhook_id/$discord_webhook_token"
