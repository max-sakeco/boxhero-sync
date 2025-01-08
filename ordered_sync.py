
from loguru import logger
from sync_service import SyncService
from supabase_sync import SupabaseSync

def run_ordered_sync():
    logger.info("Starting ordered sync process")
    
    # 1. BoxHero -> Postgres -> Supabase
    try:
        logger.info("Starting BoxHero sync")
        # Add BoxHero sync here when needed
        logger.info("BoxHero sync completed")
    except Exception as e:
        logger.error(f"BoxHero sync failed: {str(e)}")
        raise

    # 2. Shopify -> Postgres -> Supabase
    try:
        # Sync Shopify data to Postgres
        logger.info("Starting Shopify to Postgres sync")
        service = SyncService()
        service.sync_products()
        service.sync_recent_sales()
        logger.info("Shopify to Postgres sync completed")

        # Sync Postgres to Supabase
        logger.info("Starting Postgres to Supabase sync")
        supabase = SupabaseSync()
        supabase.sync_all()
        logger.info("Postgres to Supabase sync completed")
    except Exception as e:
        logger.error(f"Sync failed: {str(e)}")
        raise

if __name__ == "__main__":
    run_ordered_sync()
