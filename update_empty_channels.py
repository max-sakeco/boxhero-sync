
from models import get_session, ShopifySale
from shopify_client import ShopifyClient
from loguru import logger

def update_empty_channels():
    session = get_session()
    client = ShopifyClient()
    
    # Get all sales with empty sales_channel
    empty_channel_sales = session.query(ShopifySale).filter(
        (ShopifySale.sales_channel.is_(None)) | 
        (ShopifySale.sales_channel == '')
    ).all()
    
    logger.info(f"Found {len(empty_channel_sales)} sales with empty channels")
    
    # Update each sale
    for sale in empty_channel_sales:
        logger.info(f"Processing order {sale.order_name}")
        
        # Fetch order details from Shopify
        for order in client.iter_recent_orders(days=365):
            if order['id'] == sale.shopify_order_id:
                sale.sales_channel = order.get('sales_channel')
                logger.info(f"Updated sales channel to: {sale.sales_channel}")
                break
    
    session.commit()
    logger.info("Finished updating sales channels")

if __name__ == "__main__":
    update_empty_channels()
