
from supabase_service import SupabaseService
from loguru import logger

def verify_schema():
    try:
        supabase = SupabaseService()
        
        # Test products table structure
        products = supabase.client.rpc('test_products_schema').execute()
        
        # Test sales table structure
        sales = supabase.client.rpc('test_sales_schema').execute()
        
        # Test sale items table structure
        items = supabase.client.rpc('test_sale_items_schema').execute()
        
        logger.info("Schema verification completed successfully")
        return True
    except Exception as e:
        logger.error(f"Schema verification failed: {str(e)}")
        return False

if __name__ == "__main__":
    verify_schema()
