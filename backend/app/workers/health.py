import socket
from app.workers.celery_app import celery_app

if __name__ == '__main__':
    replies = celery_app.control.ping(destination=[f'celery@{socket.gethostname()}'], timeout=3)
    raise SystemExit(0 if replies else 1)
