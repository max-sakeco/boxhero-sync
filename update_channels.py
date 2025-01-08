
from sync_service import SyncService
from loguru import logger

if __name__ == "__main__":
    service = SyncService()
    try:
        service.update_existing_sales_channels()
        logger.info("Sales channel update completed")
    except Exception as e:
        logger.error(f"Update failed: {str(e)}")
        raise
