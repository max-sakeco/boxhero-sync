
CREATE OR REPLACE FUNCTION test_products_schema()
RETURNS boolean AS $$
BEGIN
  PERFORM column_name, data_type 
  FROM information_schema.columns 
  WHERE table_name = 'shopify_products'
  AND column_name IN ('shopify_id', 'title', 'description', 'sku', 'barcode', 'inventory_quantity', 'price', 'compare_at_price', 'image_url', 'last_synced_at', 'created_at', 'updated_at');
  RETURN FOUND;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION test_sales_schema()
RETURNS boolean AS $$
BEGIN
  PERFORM column_name, data_type 
  FROM information_schema.columns 
  WHERE table_name = 'shopify_sales'
  AND column_name IN ('shopify_order_id', 'order_name', 'created_at', 'total_price', 'sales_channel', 'synced_at');
  RETURN FOUND;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION test_sale_items_schema()
RETURNS boolean AS $$
BEGIN
  PERFORM column_name, data_type 
  FROM information_schema.columns 
  WHERE table_name = 'shopify_sale_items'
  AND column_name IN ('sale_id', 'title', 'quantity', 'original_price', 'discounted_price', 'sku', 'synced_at');
  RETURN FOUND;
END;
$$ LANGUAGE plpgsql;
