# Mariyam New Year deploy

Server path:

```bash
/home/mariyam-new-year
```

Domain:

```bash
http://mariyam-new-year.uz/
```

First deploy:

```bash
cd /home/mariyam-new-year
bash deploy/setup.sh
```

If `.env` is created for the first time, edit it and rerun setup:

```bash
nano /home/mariyam-new-year/.env
bash deploy/setup.sh
```

Restart after code updates:

```bash
cd /home/mariyam-new-year
myenv/bin/python manage.py migrate
myenv/bin/python manage.py collectstatic --noinput
systemctl restart mariyam-new-year
nginx -t && systemctl reload nginx
```

Useful checks:

```bash
systemctl status mariyam-new-year
journalctl -u mariyam-new-year -f
tail -f /var/log/mariyam-new-year/error.log
```
