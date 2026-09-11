FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# build-essential: cffi/cryptography gibi bazı paketler için hazır wheel bulunamazsa derleme
# imkanı sağlar. MySQL sürücüsü olarak PyMySQL (saf Python) kullanıldığı için
# libmysqlclient-dev gibi native bir bağımlılık gerekmiyor.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
CMD ["gunicorn", "fasonbul.wsgi:application", "--bind", "0.0.0.0:8000"]
