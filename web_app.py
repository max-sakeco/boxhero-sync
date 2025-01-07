from flask import Flask, render_template_string
from models import get_session, Item
import json
import os

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>BoxHero Inventory</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.datatables.net/1.11.5/css/dataTables.bootstrap5.min.css" rel="stylesheet">
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://cdn.datatables.net/1.11.5/js/jquery.dataTables.min.js"></script>
    <script src="https://cdn.datatables.net/1.11.5/js/dataTables.bootstrap5.min.js"></script>
    <style>
        .low-stock { color: red; }
        .zero-stock { background-color: #ffebee; }
    </style>
</head>
<body>
    <div class="container-fluid mt-4">
        <h1>BoxHero Inventory</h1>
        <div class="row mb-3">
            <div class="col">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Inventory Summary</h5>
                        <p class="card-text">
                            Total Items: {{ total_items }}<br>
                            Total Quantity: {{ total_quantity }}<br>
                            Items with Stock: {{ items_with_stock }}<br>
                            Items with Zero Stock: {{ items_zero_stock }}
                        </p>
                    </div>
                </div>
            </div>
        </div>
        <div class="table-responsive">
            <table id="inventory-table" class="table table-striped table-bordered">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>SKU</th>
                        <th>Quantity</th>
                        <th>Location</th>
                        <th>Brand</th>
                        <th>Storage Type</th>
                        <th>Min Stock</th>
                        <th>Client SKU</th>
                        <th>Entry Date</th>
                    </tr>
                </thead>
                <tbody>
                    {% for item in items %}
                    <tr {% if item.quantity == 0 %}class="zero-stock"{% endif %}>
                        <td>{{ item.name }}</td>
                        <td>{{ item.sku }}</td>
                        <td {% if item.quantity < item.min_stock %}class="low-stock"{% endif %}>
                            {{ item.quantity }}
                            {% if item.min_stock and item.quantity < item.min_stock %}
                            <span class="badge bg-warning">Low Stock</span>
                            {% endif %}
                        </td>
                        <td>{{ item.location }}</td>
                        <td>{{ item.brand }}</td>
                        <td>{{ item.storage_type }}</td>
                        <td>{{ item.min_stock }}</td>
                        <td>{{ item.client_sku }}</td>
                        <td>{{ item.entry_date }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
    <script>
        $(document).ready(function() {
            $('#inventory-table').DataTable({
                pageLength: 25,
                order: [[0, 'asc']],
                dom: 'Bfrtip',
                buttons: ['copy', 'csv', 'excel']
            });
        });
    </script>
</body>
</html>
"""

def get_attr_value(attrs, name):
    """Helper function to get attribute value from attrs list"""
    if not attrs:
        return ""
    for attr in attrs:
        if attr.get('name') == name:
            return attr.get('value', '')
    return ""

@app.route('/')
def index():
    session = get_session()
    items_query = session.query(Item).all()
    
    # Process items
    items = []
    total_quantity = 0
    items_with_stock = 0
    items_zero_stock = 0
    
    for item in items_query:
        quantity = item.quantity or 0
        total_quantity += quantity
        if quantity > 0:
            items_with_stock += 1
        else:
            items_zero_stock += 1
            
        # Extract attributes
        attrs = item.attrs or []
        min_stock = get_attr_value(attrs, 'Minimum Stock')
        min_stock = int(min_stock) if min_stock and min_stock.isdigit() else None
        
        items.append({
            'name': item.name,
            'sku': item.sku,
            'quantity': quantity,
            'location': get_attr_value(attrs, 'Location'),
            'brand': get_attr_value(attrs, 'Brand'),
            'storage_type': get_attr_value(attrs, 'Storage Type'),
            'min_stock': min_stock,
            'client_sku': get_attr_value(attrs, 'CLIENT SKU'),
            'entry_date': get_attr_value(attrs, 'Date of Entry')
        })
    
    session.close()
    
    return render_template_string(
        HTML_TEMPLATE,
        items=items,
        total_items=len(items),
        total_quantity=total_quantity,
        items_with_stock=items_with_stock,
        items_zero_stock=items_zero_stock
    )

if __name__ == '__main__':
    # Get port from environment variable for Replit
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
