from shopify_client import ShopifyClient
from loguru import logger

def test_orders():
    try:
        client = ShopifyClient()
        logger.info("Fetching orders from Shopify...")
        count = 0
        for order in client.iter_recent_orders(days=30):
            count += 1
            logger.info(f"\nOrder #{count}:")
            logger.info(f"Order Name: {order['order_name']}")
            logger.info(f"Order ID: {order['id']}")
            logger.info(f"Created At: {order['created_at']}")
            logger.info(f"Total Price: {order['total_price']}")
            logger.info(f"Sales Channel: {order.get('sales_channel', 'N/A')}")
            logger.info("Items:")
            for item in order['items']:
                logger.info(f"- {item['title']} (x{item['quantity']}) @ {item['original_price']}")

            if count >= 5:  # Limit to first 5 orders for testing
                break

        if count == 0:
            logger.warning("No orders found in Shopify")

    except Exception as e:
        logger.error(f"Error testing orders: {str(e)}")
        logger.error(f"Error type: {type(e)}")
        raise

if __name__ == "__main__":
    test_orders()