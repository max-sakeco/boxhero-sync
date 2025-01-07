import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
BOXHERO_API_BASE_URL = "https://rest.boxhero-app.com/v1"
BOXHERO_API_KEY = os.getenv("BOXHERO_API_KEY")

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost:5432/boxhero").replace("postgres://", "postgresql://")

# Sync Configuration
SYNC_INTERVAL_MINUTES = int(os.getenv("SYNC_INTERVAL_MINUTES", "60"))
BATCH_SIZE = 100  # Number of records to process in each batch

# Retry Configuration
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = "sync.log"
