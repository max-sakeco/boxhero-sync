
from boxhero_client import BoxHeroClient
from loguru import logger

def test_connection():
    try:
        client = BoxHeroClient()
        response = client.get_inventory()
        logger.info("Successfully connected to BoxHero API!")
        logger.info(f"Retrieved {len(response.get('items', []))} items")
        return True
    except Exception as e:
        logger.error(f"Failed to connect to BoxHero API: {str(e)}")
        return False

if __name__ == "__main__":
    test_connection()
