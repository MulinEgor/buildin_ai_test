import asyncio
import logging

from core.database import init_prisma
from worker.worker import celery_app
from core.analyzer.dependencies import get_analyzer_service
from core.logger import setup_logging


@celery_app.task
def run_analysis():
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("Starting analysis task")
    try:
        service = get_analyzer_service()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(init_prisma())
        loop.run_until_complete(service.analyze())
        loop.close()
        logger.info("Analysis task completed successfully")
    except Exception as e:
        logger.error(f"Error in analysis task: {e}")
        raise
    