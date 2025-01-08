
import shopify
from loguru import logger
import os
from typing import Generator, Dict

class ShopifyClient:
    def __init__(self):
        shop_url = os.getenv('SHOPIFY_SHOP_URL')
        api_key = os.getenv('SHOPIFY_API_KEY')
        password = os.getenv('SHOPIFY_PASSWORD')
        
        if not all([shop_url, api_key, password]):
            raise ValueError("Shopify credentials not found in environment")
            
        shop_url = f"https://{api_key}:{password}@{shop_url}"
        shopify.ShopifyResource.set_site(shop_url)
        
    def iter_all_products(self) -> Generator[Dict, None, None]:
        """Iterator to fetch all products"""
        page = 1
        while True:
            products = shopify.Product.find(limit=250, page=page)
            if not products:
                break
                
            for product in products:
                yield {
                    'id': str(product.id),
                    'name': product.title,
                    'sku': getattr(product.variants[0], 'sku', None),
                    'barcode': getattr(product.variants[0], 'barcode', None),
                    'quantity': int(getattr(product.variants[0], 'inventory_quantity', 0)),
                    'price': str(getattr(product.variants[0], 'price', 0)),
                    'cost': str(getattr(product.variants[0], 'cost', 0)),
                    'photo_url': product.images[0].src if product.images else None,
                    'attrs': []
                }
            
            page += 1
            
    def get_product(self, product_id: str) -> Dict:
        """Fetch a specific product"""
        product = shopify.Product.find(product_id)
        return {
            'id': str(product.id),
            'name': product.title,
            'sku': getattr(product.variants[0], 'sku', None),
            'barcode': getattr(product.variants[0], 'barcode', None),
            'quantity': int(getattr(product.variants[0], 'inventory_quantity', 0)),
            'price': str(getattr(product.variants[0], 'price', 0)),
            'cost': str(getattr(product.variants[0], 'cost', 0)),
            'photo_url': product.images[0].src if product.images else None,
            'attrs': []
        }
