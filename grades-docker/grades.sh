#!/bin/bash
 
python3 -m campusnet $USERNAME $PASSWORD -o table > /tmp/grades.txt
if [ ! -s grades.txt ]; then
    mv /tmp/grades.txt grades.txt
    exit 0
fi
/usr/bin/diff grades.txt /tmp/grades.txt > /tmp/diff.txt
if [ -s /tmp/diff.txt ]; then
    (echo -e "From: Grades <${USERNAME}>\nSubject: Grades changed\n\n"; cat /tmp/diff.txt; echo -e '\n\nAll grades:\n'; cat /tmp/grades.txt) | /usr/sbin/sendmail $NOTIFY_RECIPIENT
    echo "$(date +"%b %d %H:%M:%S") $HOSTNAME grades.sh[$$]: Sent mail to ${NOTIFY_RECIPIENT}."
else
    echo "$(date +"%b %d %H:%M:%S") $HOSTNAME grades.sh[$$]: No changes detected."
fi
mv /tmp/grades.txt grades.tx