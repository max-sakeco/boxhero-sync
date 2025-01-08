
from supabase_service import SupabaseService
from loguru import logger

def verify_schema():
    try:
        supabase = SupabaseService()
        
        # Test products table
        products = supabase.client.table('shopify_products').select('*').limit(1).execute()
        logger.info("Products table schema OK")
        
        # Test sales table
        sales = supabase.client.table('shopify_sales').select('*').limit(1).execute()
        logger.info("Sales table schema OK")
        
        # Test sale items table
        items = supabase.client.table('shopify_sale_items').select('*').limit(1).execute()
        logger.info("Sale items table schema OK")
        
        logger.info("Schema verification completed successfully")
        return True
    except Exception as e:
        logger.error(f"Schema verification failed: {str(e)}")
        return False

if __name__ == "__main__":
    verify_schema()
