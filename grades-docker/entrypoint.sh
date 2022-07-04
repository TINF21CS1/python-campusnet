#! /bin/bash

# https://stackoverflow.com/a/39296583
# sets noficy_recipient to username, if not set
if [[ -z "${NOTIFY_RECIPIENT}" ]]; then
  NOTIFY_RECIPIENT="${USERNAME}"
fi

crond
echo "$(date +"%b %d %H:%M:%S") $HOSTNAME entrypoint.sh[$$]: Started crond."
echo $PASSWORD | openconnect -b --user=$USERNAME --authgroup=$AUTHGROUP --passwd-on-stdin $HOST
echo "$(date +"%b %d %H:%M:%S") $HOSTNAME entrypoint.sh[$$]: Started openconnect."
echo -e "root=${USERNAME}\nmailhub=studgate.dhbw-mannheim.de:25\nrewriteDomain=student.dhbw-mannheim.de\nhostname=${hostname}\nAuthUser=${USERNAME}\nAuthPass=${PASSWORD}\nAuthMethod=LOGIN\nFromLineOverride=no" > /etc/ssmtp/ssmtp.conf
echo -e "root:${USERNAME}:studgate.dhbw-mannheim.de:25"
chfn -f 'Campusnet Grades' root
echo "$(date +"%b %d %H:%M:%S") $HOSTNAME entrypoint.sh[$$]: Updates ssmtp configuration."

echo "$(date +"%b %d %H:%M:%S") $HOSTNAME start.sh[$$]: ➔ Switching to log output from 'grep CRON /var/log/syslog'"
tail -f grep CRON /var/log/syslog