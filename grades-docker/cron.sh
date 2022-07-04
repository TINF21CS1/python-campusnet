#!/bin/bash
 
python3 -m campusnet $USERNAME $PASSWORD -o table > /tmp/grades.txt
if [ ! -s grades.txt ]; then
    mv /tmp/grades.txt grades.txt
    exit 0
fi
/usr/bin/diff grades.txt /tmp/grades.txt > /tmp/diff.txt
if [ -s /tmp/diff.txt ]; then
    (echo -e 'Subject: Grades changed\n\n'; cat /tmp/diff.txt; echo -e '\n\nAll grades:\n'; cat /tmp/grades.txt) | /usr/sbin/sendmail $NOTIFY_RECIPIENT
fi
mv /tmp/grades.txt grades.tx