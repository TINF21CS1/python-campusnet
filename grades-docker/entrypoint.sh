#! /bin/bash

# https://stackoverflow.com/a/39296583
# sets noficy_recipient to username, if not set
if [[ -z "${NOTIFY_RECIPIENT}" ]]; then
  NOTIFY_RECIPIENT="${USERNAME}"
fi

echo $PASSWORD | openconnect -b --user=$VPNUSERNAME --authgroup=$AUTHGROUP --passwd-on-stdin $HOST
echo "$(date +"%b %d %H:%M:%S") $HOSTNAME entrypoint.sh[$$]: Started openconnect."
echo -e "root=${USERNAME}\nmailhub=studgate.dhbw-mannheim.de:25\nrewriteDomain=student.dhbw-mannheim.de\nhostname=campusnet.docker.local\nAuthUser=${USERNAME}\nAuthPass=${PASSWORD}\nAuthMethod=LOGIN\nFromLineOverride=no" > /etc/ssmtp/ssmtp.conf
echo -e "root:${USERNAME}:studgate.dhbw-mannheim.de:25" > /etc/ssmtp/revaliases
echo "$(date +"%b %d %H:%M:%S") $HOSTNAME entrypoint.sh[$$]: Updated ssmtp configuration."

echo "$(date +"%b %d %H:%M:%S") $HOSTNAME entrypoint.sh[$$]: Starting crond..."
crond -f