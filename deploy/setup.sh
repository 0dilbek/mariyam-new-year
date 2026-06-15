#!/bin/bash
set -e

PROJECT_DIR=/home/mariyam-new-year
SERVICE_NAME=mariyam-new-year
NGINX_SITE=mariyam-new-year
LOG_DIR=/var/log/mariyam-new-year

echo "=== 1. Paketlar o'rnatilmoqda ==="
apt update && apt install -y python3 python3-pip python3-venv nginx

echo "=== 2. Python venv va paketlar ==="
cd "$PROJECT_DIR"
if [ ! -d myenv ]; then
    python3 -m venv myenv
fi
myenv/bin/pip install --upgrade pip
myenv/bin/pip install gunicorn
myenv/bin/pip install -r requirements.txt

echo "=== 3. .env fayl ==="
if [ ! -f .env ]; then
    cp deploy/.env.example .env
    echo ">>> .env faylni to'ldiring: nano $PROJECT_DIR/.env"
    exit 1
fi

echo "=== 4. Django setup ==="
myenv/bin/python manage.py migrate
myenv/bin/python manage.py collectstatic --noinput

echo "=== 5. Log papka ==="
mkdir -p "$LOG_DIR"
chown www-data:www-data "$LOG_DIR"

echo "=== 6. Gunicorn service ==="
cp deploy/gunicorn.service "/etc/systemd/system/$SERVICE_NAME.service"
systemctl daemon-reload
systemctl enable "$SERVICE_NAME"
systemctl restart "$SERVICE_NAME"

echo "=== 7. Nginx sozlash ==="
cp deploy/nginx.conf "/etc/nginx/sites-available/$NGINX_SITE"
ln -sf "/etc/nginx/sites-available/$NGINX_SITE" "/etc/nginx/sites-enabled/$NGINX_SITE"
nginx -t
systemctl reload nginx

echo ""
echo "✓ Deploy tugadi!"
echo "  Domain: http://mariyam-new-year.uz/"
echo ""
echo "Status tekshirish:"
echo "  systemctl status $SERVICE_NAME"
echo "  journalctl -u $SERVICE_NAME -f"
