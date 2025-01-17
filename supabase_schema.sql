
CREATE TABLE IF NOT EXISTS shopify_products (
    id SERIAL PRIMARY KEY,
    shopify_id VARCHAR UNIQUE NOT NULL,
    title VARCHAR NOT NULL,
    description TEXT,
    sku VARCHAR,
    barcode VARCHAR,
    inventory_quantity INTEGER DEFAULT 0,
    price DECIMAL(10,2),
    compare_at_price DECIMAL(10,2),
    image_url VARCHAR,
    last_synced_at TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS shopify_sales (
    id SERIAL PRIMARY KEY,
    shopify_order_id VARCHAR NOT NULL,
    order_name VARCHAR,
    created_at TIMESTAMPTZ,
    total_price DECIMAL(10,2),
    sales_channel VARCHAR,
    synced_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS shopify_sale_items (
    id SERIAL PRIMARY KEY,
    sale_id INTEGER REFERENCES shopify_sales(id),
    title VARCHAR NOT NULL,
    quantity INTEGER,
    original_price DECIMAL(10,2),
    discounted_price DECIMAL(10,2),
    sku VARCHAR,
    synced_at TIMESTAMPTZ DEFAULT NOW()
);

-- Refresh schema cache
ALTER TABLE shopify_sale_items ADD COLUMN IF NOT EXISTS synced_at TIMESTAMPTZ DEFAULT NOW();
NOTIFY pgrst, 'reload schema';

CREATE TABLE IF NOT EXISTS sync_logs (
    id SERIAL PRIMARY KEY,
    start_time TIMESTAMPTZ NOT NULL,
    end_time TIMESTAMPTZ,
    status VARCHAR,
    records_processed INTEGER DEFAULT 0,
    error_message VARCHAR
);
