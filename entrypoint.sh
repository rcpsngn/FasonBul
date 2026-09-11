#!/bin/sh
set -e

# DB_ENGINE=mysql ise, container'lar aynı anda ayağa kalktığında web servisinin
# MySQL henüz hazır olmadan bağlanmaya çalışmasını önlemek için portu bekleriz.
if [ "$DB_ENGINE" = "mysql" ]; then
    echo "MySQL'in hazır olması bekleniyor ($DB_HOST:$DB_PORT)..."
    python - <<'PYEOF'
import os
import socket
import sys
import time

host = os.environ.get("DB_HOST", "127.0.0.1")
port = int(os.environ.get("DB_PORT", "3306"))

for _ in range(60):
    try:
        with socket.create_connection((host, port), timeout=2):
            break
    except OSError:
        time.sleep(1)
else:
    sys.exit(f"MySQL'e bağlanılamadı ({host}:{port}), zaman aşımı.")
PYEOF
    echo "MySQL hazır."
fi

echo "Migration'lar uygulanıyor..."
python manage.py migrate --noinput

if [ "$DEBUG" != "True" ]; then
    echo "Statik dosyalar toplanıyor..."
    python manage.py collectstatic --noinput
fi

exec "$@"
