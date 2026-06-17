#!/bin/bash
set -e

APP_DIR="/var/www/geeks_quiz"
SERVICE="geeks_quiz"

echo "=== Geeks Quiz Deploy ==="
cd "$APP_DIR"

echo "[1/7] Backup database..."
cp db.sqlite3 "db.sqlite3.backup.$(date +%Y%m%d_%H%M%S)" || true

echo "[2/7] Git pull..."
git pull origin main || git pull origin master

echo "[3/7] Install dependencies..."
source venv/bin/activate
pip install -r requirements.txt

echo "[4/7] Migrate..."
python manage.py migrate --noinput

echo "[5/7] Collect static..."
python manage.py collectstatic --noinput

echo "[6/7] Django check..."
python manage.py check --deploy || python manage.py check

echo "[7/7] Restart service..."
sudo systemctl restart "$SERVICE"
sudo systemctl status "$SERVICE" --no-pager

echo "=== Deploy tugadi ==="
curl -sI https://test.pyblog.uz/ | head -5
