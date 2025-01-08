
from supabase import create_client
import os
from loguru import logger

class SupabaseService:
    def __init__(self):
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_KEY')
        if not supabase_url or not supabase_key:
            raise ValueError("Supabase credentials not found in environment")
        self.client = create_client(supabase_url, supabase_key)

    def sync_item(self, item_data: dict):
        try:
            self.client.table('boxhero').upsert({
                'boxhero_id': item_data['boxhero_id'],
                'name': item_data['name'],
                'sku': item_data['sku'],
                'barcode': item_data['barcode'],
                'photo_url': item_data['photo_url'],
                'cost': item_data['cost'],
                'price': item_data['price'],
                'quantity': item_data['quantity'],
                'attrs': item_data['attrs']
            }).execute()
            logger.info(f"Synced item to Supabase: {item_data['name']}")
        except Exception as e:
            logger.error(f"Error syncing to Supabase: {str(e)}")
            raise
