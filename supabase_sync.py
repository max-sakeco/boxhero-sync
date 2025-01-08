
from supabase_service import SupabaseService
from models import get_session, Product, Sale, SaleItem, SyncLog
from loguru import logger

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
                'last_synced_at': product.last_synced_at.isoformat(),
                'created_at': product.created_at.isoformat(),
                'updated_at': product.updated_at.isoformat()
            }, on_conflict='shopify_id').execute()
        logger.info(f"Synced {len(products)} products to Supabase")

    def sync_sales(self):
        sales = self.session.query(Sale).all()
        for sale in sales:
            # Insert sale
            sale_data = {
                'shopify_order_id': sale.shopify_order_id,
                'order_name': sale.order_name,
                'created_at': sale.created_at.isoformat(),
                'total_price': float(sale.total_price) if sale.total_price else None,
                'synced_at': sale.synced_at.isoformat()
            }
            result = self.supabase.client.table('sales').upsert(
                sale_data, 
                on_conflict='shopify_order_id'
            ).execute()
            
            # Get Supabase sale id
            supabase_sale_id = result.data[0]['id']
            
            # Insert sale items
            for item in sale.items:
                self.supabase.client.table('sale_items').upsert({
                    'sale_id': supabase_sale_id,
                    'title': item.title,
                    'quantity': item.quantity,
                    'original_price': float(item.original_price) if item.original_price else None,
                    'discounted_price': float(item.discounted_price) if item.discounted_price else None,
                    'sku': item.sku
                }).execute()
        
        logger.info(f"Synced {len(sales)} sales to Supabase")

    def sync_all(self):
        try:
            logger.info("Starting Supabase sync")
            self.sync_products()
            self.sync_sales()
            logger.info("Supabase sync completed")
        except Exception as e:
            logger.error(f"Supabase sync failed: {str(e)}")
            raise

if __name__ == "__main__":
    sync = SupabaseSync()
    sync.sync_all()
