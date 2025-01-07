# BoxHero Inventory Sync

A web application that syncs and displays inventory data from BoxHero API. Built with Flask and SQLite, deployable on Replit.

## Features

- Syncs inventory data from BoxHero API
- Displays inventory in a searchable, sortable table
- Shows stock levels and alerts for low stock
- Provides inventory summary statistics
- Handles cursor-based pagination for complete data retrieval

## Tech Stack

- Python 3.10+
- Flask for web interface
- SQLAlchemy for database ORM
- SQLite for local data storage
- Bootstrap 5 for UI
- DataTables for interactive tables

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/boxhero-sync.git
cd boxhero-sync
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file with:
```
BOXHERO_API_KEY=your_api_key_here
```

4. Run the sync:
```bash
python -c "from sync_service import SyncService; SyncService().sync()"
```

5. Start the web app:
```bash
python web_app.py
```

Visit `http://localhost:5000` to view your inventory.

## Deploying to Replit

1. Import from GitHub to Replit
2. Add your BoxHero API key in Replit Secrets
3. Click Run

## Development

- `boxhero_client.py`: BoxHero API client
- `models.py`: Database models
- `sync_service.py`: Data synchronization service
- `web_app.py`: Flask web application

## License

MIT License
