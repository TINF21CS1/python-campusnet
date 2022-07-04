# Campusnet Grade Notifier

This docker container will check your grade every hour and send a notification mail, if something has changed. Currently this docker container is very tailored for DHBW-Mannheim students. But feel free to broaden its usability with a PR.

## Usage

3 Environment variables are needed:

* `USERNAME`: Your student mail address with the domain part. That is also used to login to CampusNet (Dualis)
* `VPNUSERNAME`: Your username without the domain part. Used for the login with Anyconnect VPN, to send mails.
* `PASSWORD`: Your account password. Used for VPN, Campusnet and Mail authentication.
* Optional `NOTIFY_RECIPIENT`: Mail address that will receive notifications. By default the same as `USERNAME`.

```
docker run --privileged -e "USERNAME=s212689@student.dhbw-mannheim.de" -e "VPNUSERNAME=s212689" -e "PASSWORD=xxxxxxxxxxxxxxxx" ghcr.io/tinf21cs1/campusnet-grade-notifier
```

`--privileged` is needed for the VPN connection.

## Process

On startup a VPN connection to `drogon.dhbw-mannheim.de` is established to allow for sending mails with SMTP.

Every hour a cronjob will connect to CampusNet and download the latest grades. These will be compared to the last known state, that is saved in `/app/grades.txt`

If something changed, sendmail is used to send the diff to the `NOTIFIER_RECIPIENT`, via `studgate.dhbw-mannheim.de:25`, authenticated as `USERNAME`.
