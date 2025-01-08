from datetime import datetime
from typing import Optional
from loguru import logger
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from models import Item, SyncLog, get_session
from boxhero_client import BoxHeroClient
from supabase_service import SupabaseService

class SyncService:
    def __init__(self):
        self.client = BoxHeroClient()
        self.session = get_session()
        self.supabase = SupabaseService()

    def _create_sync_log(self) -> SyncLog:
        """Create a new sync log entry"""
        sync_log = SyncLog(start_time=datetime.utcnow(), status="running")
        self.session.add(sync_log)
        self.session.commit()
        return sync_log

    def _update_sync_log(self, sync_log: SyncLog, status: str, error_message: Optional[str] = None):
        """Update sync log with final status"""
        sync_log.end_time = datetime.utcnow()
        sync_log.status = status
        sync_log.error_message = error_message
        self.session.commit()

    def _process_item(self, item_data: dict) -> None:
        """Process a single item"""
        try:
            # Get or create item
            item = self.session.query(Item).filter_by(boxhero_id=str(item_data["id"])).first()
            
            # Prepare item data
            item_attrs = {
                "boxhero_id": str(item_data["id"]),
                "name": item_data["name"],
                "sku": item_data.get("sku"),
                "barcode": item_data.get("barcode"),
                "photo_url": item_data.get("photo_url"),
                "cost": item_data.get("cost", "0"),
                "price": item_data.get("price", "0"),
                "quantity": item_data.get("quantity", 0),
                "attrs": item_data.get("attrs", [])
            }

            if not item:
                item = Item(**item_attrs)
                self.session.add(item)
                logger.info(f"Created new item: {item_data['name']}")
            else:
                # Update existing item
                for key, value in item_attrs.items():
                    setattr(item, key, value)
                logger.info(f"Updated existing item: {item_data['name']}")

            self.session.commit()
            
            # Sync to Supabase
            self.supabase.sync_item(item_attrs)

        except Exception as e:
            self.session.rollback()
            logger.error(f"Error processing item {item_data.get('id')}: {str(e)}")
            raise

    def sync(self) -> None:
        """Main sync process"""
        sync_log = self._create_sync_log()
        records_processed = 0

        try:
            for item_data in self.client.iter_all_inventory():
                self._process_item(item_data)
                records_processed += 1
                
                if records_processed % 100 == 0:
                    logger.info(f"Processed {records_processed} items")

            sync_log.records_processed = records_processed
            self._update_sync_log(sync_log, "completed")
            logger.info(f"Sync completed successfully. Processed {records_processed} items.")

        except Exception as e:
            self._update_sync_log(sync_log, "failed", str(e))
            logger.error(f"Sync failed: {str(e)}")
            raise

        finally:
            self.session.close()
