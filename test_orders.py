
from shopify_client import ShopifyClient
from loguru import logger

def test_orders():
    try:
        client = ShopifyClient()
        # Get first order
        query = """
        query {
            orders(first: 1) {
                edges {
                    node {
                        id
                        name
                        createdAt
                        totalPrice {
                            amount
                            currencyCode
                        }
                        lineItems(first: 1) {
                            edges {
                                node {
                                    title
                                    quantity
                                    originalUnitPrice {
                                        amount
                                        currencyCode
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        """
        result = client._execute_query(query)
        logger.info("Raw Shopify Response:")
        logger.info(result)
        
        if 'data' in result and 'orders' in result['data']:
            orders = result['data']['orders']
            if orders['edges']:
                order = orders['edges'][0]['node']
                logger.info(f"Order details:")
                logger.info(f"ID: {order['id']}")
                logger.info(f"Name: {order['name']}")
                logger.info(f"Total Price: {order['totalPrice']}")
    except Exception as e:
        logger.error(f"Error testing orders: {str(e)}")
        raise

if __name__ == "__main__":
    test_orders()
