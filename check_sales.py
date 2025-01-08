
from models import get_session, Sale
from tabulate import tabulate
from datetime import datetime

def check_sales():
    session = get_session()
    sales = session.query(Sale).all()
    
    if not sales:
        print("No sales records found in the database.")
        return
    
    rows = []
    for sale in sales:
        rows.append([
            sale.order_name,
            sale.shopify_order_id,
            sale.created_at.strftime('%Y-%m-%d %H:%M') if sale.created_at else 'N/A',
            f"${sale.total_price:.2f}" if sale.total_price else '$0.00'
        ])
    
    headers = ["Order Name", "Shopify ID", "Created At", "Total Price"]
    print("\nSales Records:")
    print(tabulate(rows, headers=headers, tablefmt="grid"))
    print(f"\nTotal Records: {len(rows)}")
    
    session.close()

if __name__ == "__main__":
    check_sales()
