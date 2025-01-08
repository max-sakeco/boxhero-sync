
from datetime import datetime, timedelta
from typing import Optional
from loguru import logger
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from decimal import Decimal

from models import Product, Sale, SaleItem, SyncLog, get_session
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
                product.price = Decimal(product_data.get('price', '0'))
                product.compare_at_price = Decimal(product_data.get('cost', '0'))
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
            for order_data in self.client.iter_recent_orders(days=days):
                # Skip if order already exists
                if self.session.query(Sale).filter_by(shopify_order_id=order_data['id']).first():
                    continue
                    
                sale = Sale(
                    shopify_order_id=order_data['id'],
                    order_name=order_data['order_name'],
                    created_at=datetime.fromisoformat(order_data['created_at'].replace('Z', '+00:00')),
                    total_price=Decimal(order_data['total_price'])
                )
                self.session.add(sale)
                self.session.flush()  # Get sale.id
                
                for item in order_data['items']:
                    sale_item = SaleItem(
                        sale_id=sale.id,
                        title=item['title'],
                        quantity=item['quantity'],
                        original_price=Decimal(item['original_price']),
                        discounted_price=Decimal(item['discounted_price']),
                        sku=item['sku']
                    )
                    self.session.add(sale_item)
                
                sync_log.records_processed = (sync_log.records_processed or 0) + 1
                
            self.session.commit()
            self._update_sync_log(sync_log, "completed")
            
        except Exception as e:
            self.session.rollback()
            self._update_sync_log(sync_log, "failed", str(e))
            raise
        finally:
            self.session.close()
