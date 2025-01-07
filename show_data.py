from models import get_session, Item
from tabulate import tabulate
import json

def format_attrs(attrs):
    if not attrs:
        return ""
    return "\n".join([f"{attr['name']}: {attr['value']}" for attr in attrs])

def show_items():
    session = get_session()
    items = session.query(Item).order_by(Item.name).all()
    
    # Format data for display
    rows = []
    for item in items:
        rows.append([
            item.name,
            item.sku,
            item.quantity,
            item.cost,
            item.price,
            format_attrs(item.attrs)
        ])
    
    # Print table
    headers = ["Name", "SKU", "Quantity", "Cost", "Price", "Attributes"]
    print("\nInventory Items:")
    print(tabulate(rows, headers=headers, tablefmt="grid"))
    print(f"\nTotal Items: {len(rows)}")
    
    session.close()

if __name__ == "__main__":
    show_items()
