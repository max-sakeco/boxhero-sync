
from sync_service import SyncService
from loguru import logger

def run_daily_sync():
    service = SyncService()
    try:
        # Only sync sales for testing
        service.sync_recent_sales(days=1)
        logger.info("Sales sync completed successfully")
    except Exception as e:
        logger.error(f"Daily sync failed: {str(e)}")
        raise

if __name__ == "__main__":
    run_daily_sync()
