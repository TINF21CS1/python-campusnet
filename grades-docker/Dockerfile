#get vpn client
FROM ghcr.io/jm-lemmi/anyconnect-simple

# install python and package
RUN apk --update add git python3
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools
RUN pip install git+https://github.com/TINF21CS1/python-campusnet@dev

# Add crontab
COPY grades.sh /app/grades.sh
RUN crontab -l /cron
RUN echo "0 7-23 * * * /app/grades.sh" >> /cron
RUN crontab /cron
RUN rm /cron

#ENV USERNAME "s:)@student.dhbw-mannheim.de"
#ENV PASSWORD='***'
#ENV NOTIFY_RECIPIENT="***"
#default values for dhbw mannheim
ENV AUTHGROUP Studenten
ENV HOST drogon.dhbw-mannheim.de

# add sendmail
RUN apk add ssmtp

COPY entrypoint.sh /app/entrypoint.sh
CMD /bin/sh /app/entrypoint.sh