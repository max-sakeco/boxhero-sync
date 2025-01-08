
from sync_service import SyncService
from loguru import logger

def run_daily_sync():
    service = SyncService()
    try:
        # Run sales sync first
        logger.info("Starting sales sync")
        service.sync_recent_sales(days=1)
        logger.info("Sales sync completed")
        
        # Then run product sync
        logger.info("Starting product sync")
        service.sync_products()
        logger.info("Product sync completed")
    except Exception as e:
        logger.error(f"Sync failed: {str(e)}")
        raise

if __name__ == "__main__":
    run_daily_sync()
