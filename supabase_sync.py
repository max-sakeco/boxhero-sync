from supabase_service import SupabaseService
from models import get_session, Product, ShopifySale, ShopifySaleItem, SyncLog
from loguru import logger
from datetime import datetime, timezone as datetime_timezone

class SupabaseSync:
    def __init__(self):
        self.supabase = SupabaseService()
        self.session = get_session()

    def sync_products(self):
        products = self.session.query(Product).all()
        for product in products:
            self.supabase.client.table('shopify_products').upsert({
                'shopify_id': product.shopify_id,
                'title': product.title,
                'description': product.description,
                'sku': product.sku,
                'barcode': product.barcode,
                'inventory_quantity': product.inventory_quantity,
                'price': float(product.price) if product.price else None,
                'compare_at_price': float(product.compare_at_price) if product.compare_at_price else None,
                'image_url': product.image_url,
                'last_synced_at': product.last_synced_at.isoformat() if product.last_synced_at else None,
                'created_at': product.created_at.isoformat() if product.created_at else None,
                'updated_at': product.updated_at.isoformat() if product.updated_at else None
            }, on_conflict='shopify_id').execute()
        logger.info(f"Synced {len(products)} products to Supabase")

    def sync_sales(self):
        sales = self.session.query(ShopifySale).all()
        for sale in sales:
            # Insert sale
            sale_result = self.supabase.client.table('shopify_sales').upsert({
                'shopify_order_id': sale.shopify_order_id,
                'order_name': sale.order_name,
                'created_at': sale.created_at.isoformat() if sale.created_at else None,
                'total_price': float(sale.total_price) if sale.total_price else None,
                'sales_channel': sale.sales_channel,
                'synced_at': datetime.now(datetime_timezone.utc).isoformat()
            }, on_conflict='shopify_order_id').execute()

            # Get the Supabase sale ID from the response
            supabase_sale = sale_result.data[0]

            # Sync sale items
            for item in sale.items:
                self.supabase.client.table('shopify_sale_items').upsert({
                    'sale_id': supabase_sale['id'],
                    'title': item.title,
                    'quantity': item.quantity,
                    'original_price': float(item.original_price) if item.original_price else None,
                    'discounted_price': float(item.discounted_price) if item.discounted_price else None,
                    'sku': item.sku,
                    'synced_at': datetime.now(datetime_timezone.utc).isoformat()
                }).execute()

        logger.info(f"Synced {len(sales)} sales to Supabase")

    def sync_all(self):
        try:
            logger.info("Starting Supabase sync")
            self.sync_products()
            self.sync_sales()
            logger.info("Supabase sync completed successfully")
        except Exception as e:
            logger.error(f"Supabase sync failed: {str(e)}")
            raise

if __name__ == "__main__":
    sync = SupabaseSync()
    sync.sync_all()