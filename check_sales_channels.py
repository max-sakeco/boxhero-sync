
from models import get_session, ShopifySale
from tabulate import tabulate
from loguru import logger

def check_sales_channels():
    session = get_session()
    sales = session.query(ShopifySale).all()
    
    empty_channels = 0
    rows = []
    
    for sale in sales:
        channel = sale.sales_channel if sale.sales_channel else 'EMPTY'
        if not sale.sales_channel:
            empty_channels += 1
            
        rows.append([
            sale.order_name,
            channel,
            sale.created_at.strftime('%Y-%m-%d %H:%M') if sale.created_at else 'N/A'
        ])
    
    headers = ["Order Name", "Sales Channel", "Created At"]
    print("\nSales Channel Status:")
    print(tabulate(rows, headers=headers, tablefmt="grid"))
    print(f"\nTotal Records: {len(rows)}")
    print(f"Empty Channels: {empty_channels}")
    
    session.close()

if __name__ == "__main__":
    check_sales_channels()
