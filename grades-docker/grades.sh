#!/bin/bash

echo $PASSWORD | openconnect -b --user=$VPNUSERNAME --authgroup=$AUTHGROUP --passwd-on-stdin $HOST
echo "$(date +"%b %d %H:%M:%S") $HOSTNAME grades.sh[$$]: Started openconnect in background."
 
 echo "$(date +"%b %d %H:%M:%S") $HOSTNAME grades.sh[$$]: Getting grades from Campusnet."
python3 -m campusnet $USERNAME $PASSWORD -o table > /tmp/grades.txt
if [ ! -s grades.txt ]; then
    mv /tmp/grades.txt grades.txt
    echo "$(date +"%b %d %H:%M:%S") $HOSTNAME grades.sh[$$]: First run, created grades.txt."
    exit 0
fi
/usr/bin/diff grades.txt /tmp/grades.txt > /tmp/diff.txt
if [ -s /tmp/diff.txt ]; then
    (echo -e "From: Grades <${USERNAME}>\nSubject: Grades changed\n\n"; cat /tmp/diff.txt; echo -e '\n\nAll grades:\n'; cat /tmp/grades.txt) | /usr/sbin/sendmail $NOTIFY_RECIPIENT
    echo "$(date +"%b %d %H:%M:%S") $HOSTNAME grades.sh[$$]: Sent mail to ${NOTIFY_RECIPIENT}."
else
    echo "$(date +"%b %d %H:%M:%S") $HOSTNAME grades.sh[$$]: No changes detected."
fi
mv /tmp/grades.txt grades.txt

/usr/bin/killall openconnect
echo "$(date +"%b %d %H:%M:%S") $HOSTNAME grades.sh[$$]: Killed openconnect."
