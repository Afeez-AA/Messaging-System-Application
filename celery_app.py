from celery import Celery
from config import Config

celery_app = Celery('messaging_system',
                    broker=Config.BROKER_URL,
                    backend=Config.RESULT_BACKEND)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],  
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

# Import tasks to ensure they are registered
import tasks
