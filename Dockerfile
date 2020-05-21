FROM alpine:latest

WORKDIR /www/cpu_checker

COPY cpu_checker cpu_checker/
COPY requirements.txt manage.py ./

RUN set -x && \
  apk update && \
  apk add --no-cache python3 && \
  /usr/bin/pip3 install --upgrade pip && \
  /usr/bin/pip3 install -r requirements.txt

EXPOSE 8000

CMD gunicorn \
    --bind 0.0.0.0:8000 \
    --workers 2 --threads 2 \
    --worker-class gthread \
    --worker-tmp-dir /dev/shm \
    --access-logfile '-' \
    cpu_checker.wsgi
