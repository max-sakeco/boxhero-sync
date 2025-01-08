
from supabase_service import SupabaseService
from loguru import logger

def test_supabase_connection():
    try:
        supabase = SupabaseService()
        
        # Test products table
        products = supabase.client.table('shopify_products').select("*").limit(5).execute()
        logger.info(f"Products table exists. Found {len(products.data)} records")
        
        # Test sales table
        sales = supabase.client.table('shopify_sales').select("*").limit(5).execute()
        logger.info(f"Sales table exists. Found {len(sales.data)} records")
        
        # Test sale items table
        items = supabase.client.table('shopify_sale_items').select("*").limit(5).execute()
        logger.info(f"Sale items table exists. Found {len(items.data)} records")
        
        return True
    except Exception as e:
        logger.error(f"Supabase connection test failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_supabase_connection()
