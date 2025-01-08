import os
from typing import Generator, Dict
import requests
from loguru import logger

class ShopifyClient:
    def __init__(self):
        self.shop_url = os.getenv('SHOPIFY_SHOP_URL')
        self.access_token = os.getenv('SHOPIFY_API_KEY')

        if not self.shop_url or not self.access_token:
            raise ValueError("Shopify credentials not found in environment")

        self.api_url = f"https://{self.shop_url}/admin/api/2024-01/graphql.json"
        self.headers = {
            'Content-Type': 'application/json',
            'X-Shopify-Access-Token': self.access_token
        }

    def _execute_query(self, query: str, variables: dict = None) -> dict:
        response = requests.post(
            self.api_url,
            json={'query': query, 'variables': variables or {}},
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def iter_all_products(self) -> Generator[Dict, None, None]:
        query = """
        query($cursor: String) {
            products(first: 50, after: $cursor) {
                pageInfo {
                    hasNextPage
                    endCursor
                }
                edges {
                    node {
                        id
                        title
                        description
                        images(first: 1) {
                            edges {
                                node {
                                    url
                                }
                            }
                        }
                        variants(first: 1) {
                            edges {
                                node {
                                    sku
                                    barcode
                                    inventoryQuantity
                                    price
                                    compareAtPrice
                                }
                            }
                        }
                    }
                }
            }
        }
        """

        cursor = None
        while True:
            result = self._execute_query(query, {'cursor': cursor})
            products = result['data']['products']

            for edge in products['edges']:
                product = edge['node']
                variant = product['variants']['edges'][0]['node'] if product['variants']['edges'] else {}
                image_url = product['images']['edges'][0]['node']['url'] if product['images']['edges'] else None

                yield {
                    'id': product['id'].split('/')[-1],
                    'name': product['title'],
                    'description': product['description'],
                    'sku': variant.get('sku'),
                    'barcode': variant.get('barcode'),
                    'quantity': variant.get('inventoryQuantity', 0),
                    'price': str(variant.get('price', '0.00')),
                    'cost': str(variant.get('compareAtPrice', '0.00')),
                    'photo_url': image_url,
                    'attrs': []
                }

            if not products['pageInfo']['hasNextPage']:
                break
            cursor = products['pageInfo']['endCursor']

    def iter_recent_orders(self, days: int = 30) -> Generator[Dict, None, None]:
        query = """
        query($cursor: String) {
            orders(first: 50, after: $cursor, query: "created_at:>=2024-01-01") {
                pageInfo {
                    hasNextPage
                    endCursor
                }
                edges {
                    node {
                        id
                        name
                        createdAt
                        totalPrice
                        lineItems(first: 50) {
                            edges {
                                node {
                                    title
                                    quantity
                                    originalUnitPrice
                                    discountedUnitPrice
                                    sku
                                }
                            }
                        }
                    }
                }
            }
        }
        """

        cursor = None
        while True:
            result = self._execute_query(query, {'cursor': cursor})
            orders = result['data']['orders']

            for edge in orders['edges']:
                order = edge['node']
                yield {
                    'id': order['id'].split('/')[-1],
                    'order_name': order['name'],
                    'created_at': order['createdAt'],
                    'total_price': str(order.get('totalPrice', '0.00')),
                    'items': [{
                        'title': item['node']['title'],
                        'quantity': item['node']['quantity'],
                        'original_price': str(item['node'].get('originalUnitPrice', '0.00')),
                        'discounted_price': str(item['node'].get('discountedUnitPrice', '0.00')),
                        'sku': item['node'].get('sku', '')
                    } for item in order['lineItems']['edges']]
                }

            if not orders['pageInfo']['hasNextPage']:
                break
            cursor = orders['pageInfo']['endCursor']