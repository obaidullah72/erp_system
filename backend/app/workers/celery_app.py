from celery import Celery
from app.core.config import get_settings
from app.core.logging import configure_logging

configure_logging(get_settings().log_level)

celery_app = Celery('erp', broker=get_settings().redis_url.get_secret_value())
celery_app.conf.update(task_serializer='json', accept_content=['json'], result_serializer='json',
                       task_ignore_result=True, timezone='UTC', enable_utc=True,
                       broker_connection_retry_on_startup=True,
                       worker_hijack_root_logger=False)


@celery_app.task(name='erp.ping')
def ping():
    """Diagnostic only. Business jobs await real modules and an outbox."""
    return 'pong'
