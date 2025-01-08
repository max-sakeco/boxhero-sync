
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

    def _get_attr_value(self, attrs, name):
        if not attrs:
            return None
        for attr in attrs:
            if attr.get('name') == name:
                return attr.get('value')
        return None

    def sync_item(self, item_data: dict):
        try:
            attrs = item_data['attrs']
            self.client.table('boxhero').upsert({
                'boxhero_id': item_data['boxhero_id'],
                'name': item_data['name'],
                'sku': item_data['sku'],
                'barcode': item_data['barcode'],
                'photo_url': item_data['photo_url'],
                'cost': item_data['cost'],
                'price': item_data['price'],
                'quantity': item_data['quantity'],
                'attrs': attrs,
                'location': self._get_attr_value(attrs, 'Location'),
                'brand': self._get_attr_value(attrs, 'Brand'),
                'storage_type': self._get_attr_value(attrs, 'Storage Type'),
                'minimum_stock': self._get_attr_value(attrs, 'Minimum Stock'),
                'client_sku': self._get_attr_value(attrs, 'CLIENT SKU'),
                'entry_date': self._get_attr_value(attrs, 'Date of Entry')
            }).execute()
            logger.info(f"Synced item to Supabase: {item_data['name']}")
        except Exception as e:
            logger.error(f"Error syncing to Supabase: {str(e)}")
            raise
