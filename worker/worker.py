from celery import Celery
from celery.schedules import crontab
from dotenv import load_dotenv
import os


load_dotenv()


celery_app = Celery('analyzer_tasks')


celery_app.conf.update(
    broker_url=os.getenv('CELERY_BROKER_URL'),
    timezone='Europe/Moscow',
    include=['worker.task'],
    enable_utc=True,
    worker_redirect_stdouts=False
)


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    print(f"Настройка периодических задач. Анализ будет запускаться в {os.getenv('ANALYSIS_HOUR')}:{os.getenv('ANALYSIS_MINUTE')}")
    
celery_app.conf.beat_schedule = {
    'daily-analysis': {
        'task': 'worker.task.run_analysis',
        'schedule': crontab(
            hour=int(os.getenv('ANALYSIS_HOUR', 0)),
            minute=int(os.getenv('ANALYSIS_MINUTE', 0))
        )
    }
}
