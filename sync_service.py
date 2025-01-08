
from datetime import datetime, timedelta
from typing import Optional
from loguru import logger
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from decimal import Decimal
from utils import safe_decimal
from models import Product, ShopifySale, ShopifySaleItem, SyncLog, get_session
from shopify_client import ShopifyClient

class SyncService:
    def __init__(self):
        self.client = ShopifyClient()
        self.session = get_session()

    def _create_sync_log(self) -> SyncLog:
        sync_log = SyncLog(start_time=datetime.utcnow(), status="running")
        self.session.add(sync_log)
        self.session.commit()
        return sync_log

    def _update_sync_log(self, sync_log: SyncLog, status: str, error_message: Optional[str] = None):
        sync_log.end_time = datetime.utcnow()
        sync_log.status = status
        sync_log.error_message = error_message
        sync_log.records_processed = sync_log.records_processed or 0
        self.session.commit()

    def sync_products(self):
        """Sync all products"""
        sync_log = self._create_sync_log()
        try:
            for product_data in self.client.iter_all_products():
                product = self.session.query(Product).filter_by(shopify_id=product_data['id']).first()
                if not product:
                    product = Product(shopify_id=product_data['id'])
                
                product.title = product_data['name']
                product.description = product_data.get('description')
                product.sku = product_data.get('sku')
                product.barcode = product_data.get('barcode')
                product.inventory_quantity = product_data.get('quantity', 0)
                price = product_data.get('price')
                cost = product_data.get('cost')
                product.price = safe_decimal(price)
                product.compare_at_price = safe_decimal(cost)
                product.image_url = product_data.get('photo_url')
                product.last_synced_at = datetime.utcnow()

                if not product.id:
                    self.session.add(product)
                sync_log.records_processed = (sync_log.records_processed or 0) + 1
                
            self.session.commit()
            self._update_sync_log(sync_log, "completed")
            
        except Exception as e:
            self._update_sync_log(sync_log, "failed", str(e))
            raise

    def sync_recent_sales(self, days: int = 1):
        """Sync only recent sales"""
        sync_log = self._create_sync_log()
        try:
            logger.info(f"Starting sales sync for past {days} days")
            orders_count = 0
            for order_data in self.client.iter_recent_orders(days=days):
                orders_count += 1
                logger.info(f"Found order {orders_count}: {order_data['order_name']}")
                logger.info(f"Processing order: {order_data['order_name']}")
                
                # Process items one by one
                for item in order_data['items']:
                    # Skip if this specific item from this order already exists
                    # Check if sale exists
                    sale = self.session.query(ShopifySale).filter_by(
                        shopify_order_id=order_data['id']
                    ).first()
                    
                    if not sale:
                        sale = ShopifySale(
                            shopify_order_id=order_data['id'],
                            order_name=order_data['order_name'],
                            created_at=datetime.fromisoformat(order_data['created_at'].replace('Z', '+00:00')),
                            total_price=safe_decimal(order_data['total_price']),
                            sales_channel=order_data.get('sales_channel')
                        )
                        self.session.add(sale)
                        self.session.flush()
                    
                    # Check if item exists
                    existing_item = self.session.query(ShopifySaleItem).filter_by(
                        sale_id=sale.id,
                        title=item['title']
                    ).first()
                    
                    if existing_item:
                        logger.info(f"Item {item['title']} from order {order_data['order_name']} already exists, skipping")
                        continue
                        
                    logger.info(f"Processing item: {item['title']} for order {order_data['order_name']}")
                    sale_item = ShopifySaleItem(
                        sale_id=sale.id,
                        title=item['title'],
                        quantity=item['quantity'],
                        original_price=safe_decimal(item['original_price']),
                        discounted_price=safe_decimal(item['discounted_price']),
                        sku=item['sku']
                    )
                    self.session.add(sale_item)
                    
                    sync_log.records_processed = (sync_log.records_processed or 0) + 1
                    self.session.commit()
                
            if orders_count == 0:
                logger.warning("No orders found to sync")
            self._update_sync_log(sync_log, "completed")
            
        except Exception as e:
            logger.error(f"Error syncing sales: {str(e)}")
            self.session.rollback()
            self._update_sync_log(sync_log, "failed", str(e))
            raise
def update_existing_sales_channels(self):
        """Update sales channels for existing orders"""
        sync_log = self._create_sync_log()
        try:
            logger.info("Updating sales channels for existing orders")
            for order_data in self.client.iter_recent_orders(days=365):  # Get a year's worth of orders
                sale = self.session.query(ShopifySale).filter_by(
                    shopify_order_id=order_data['id']
                ).first()
                
                if sale and not sale.sales_channel:
                    sale.sales_channel = order_data.get('sales_channel')
                    logger.info(f"Updated sales channel for order {order_data['order_name']}")
                    sync_log.records_processed = (sync_log.records_processed or 0) + 1
            
            self.session.commit()
            self._update_sync_log(sync_log, "completed")
            
        except Exception as e:
            logger.error(f"Error updating sales channels: {str(e)}")
            self.session.rollback()
            self._update_sync_log(sync_log, "failed", str(e))
            raise
