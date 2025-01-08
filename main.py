import sys
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from loguru import logger

from config import SYNC_INTERVAL_MINUTES, LOG_FILE
from models import init_db
from sync_service import SyncService

# Configure logging
logger.remove()
logger.add(sys.stderr, level="INFO")
logger.add(LOG_FILE, rotation="1 day", retention="7 days", level="INFO")

def sync_job():
    """Execute the sync job"""
    logger.info("Starting sync job")
    try:
        service = SyncService()
        service.sync_products()
        service.sync_recent_sales(days=1)
    except Exception as e:
        logger.error(f"Sync job failed: {str(e)}")
    logger.info("Sync job completed")

def main():
    """Main application entry point"""
    try:
        # Initialize database
        logger.info("Initializing database")
        init_db()

        # Create scheduler
        scheduler = BlockingScheduler()
        scheduler.add_job(
            sync_job,
            'interval',
            minutes=SYNC_INTERVAL_MINUTES,
            next_run_time=datetime.now()  # Run immediately on startup
        )

        logger.info(f"Starting scheduler with {SYNC_INTERVAL_MINUTES} minute interval")
        scheduler.start()

    except KeyboardInterrupt:
        logger.info("Application shutdown requested")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
