import os

from celery import Celery

celery_app = Celery(
    'worker',
    broker=os.getenv('REDIS_URL'),
    backend=os.getenv('REDIS_URL')
)

celery_app.conf.update(
    broker_connection_retry_on_startup=True,
    redis_backend_health_check_interval=5,
)

celery_app.autodiscover_tasks(['app'], force=True)

celery_app.conf.beat_schedule = {
    "update_multiple_item_prices": {
        "task": "update_multiple_item_prices",
        "schedule": 43200.0
    }
}
