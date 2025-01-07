import requests
from typing import Dict, Optional, Generator
from tenacity import retry, stop_after_attempt, wait_exponential
from loguru import logger

from config import BOXHERO_API_BASE_URL, BOXHERO_API_KEY, MAX_RETRIES, RETRY_DELAY

class BoxHeroClient:
    def __init__(self):
        self.base_url = BOXHERO_API_BASE_URL
        self.headers = {
            "Authorization": BOXHERO_API_KEY,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        logger.debug(f"Initialized BoxHero client with base URL: {self.base_url}")

    @retry(
        stop=stop_after_attempt(MAX_RETRIES),
        wait=wait_exponential(multiplier=RETRY_DELAY)
    )
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """Make an API request with retry logic"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        logger.debug(f"Making request to: {url}")
        try:
            response = requests.get(url, headers=self.headers, params=params)
            logger.debug(f"Response status: {response.status_code}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            logger.debug(f"Response content: {getattr(e.response, 'text', 'No response content')}")
            raise

    def get_inventory(self, cursor: Optional[str] = None) -> Dict:
        """Fetch inventory data with optional cursor"""
        params = {"limit": 100}  # Maximum allowed by the API
        if cursor:
            params["cursor"] = cursor
        
        response = self._make_request("items", params)
        items = response.get("items", [])
        has_more = response.get("has_more", False)
        current_cursor = response.get("cursor")
        count = response.get("count", 0)
        
        logger.debug(f"API Response - Items: {len(items)}, Has More: {has_more}, Cursor: {current_cursor}, Count: {count}")
        logger.debug(f"Response keys: {list(response.keys())}")
        
        return response

    def iter_all_inventory(self) -> Generator[Dict, None, None]:
        """Iterator to fetch all inventory data using cursor pagination"""
        total_items = 0
        cursor = None
        page = 1
        
        while True:
            response = self.get_inventory(cursor)
            items = response.get("items", [])
            if not items:
                break

            batch_size = len(items)
            total_items += batch_size
            logger.info(f"Page {page}: Retrieved {batch_size} items (Total so far: {total_items})")

            for item in items:
                yield item

            has_more = response.get("has_more", False)
            if not has_more:
                logger.info(f"No more pages. Total items retrieved: {total_items}")
                break
                
            cursor = response.get("cursor")
            page += 1

    def get_item_details(self, item_id: str) -> Dict:
        """Fetch detailed information for a specific item"""
        return self._make_request(f"items/{item_id}")

    def get_stock_levels(self, item_id: str) -> Dict:
        """Fetch stock levels for a specific item"""
        return self._make_request(f"items/{item_id}/stocks")
