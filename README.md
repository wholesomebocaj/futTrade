# FC26 Codex

A Django + Django REST Framework project for storing EA FC 26 player data and their platform-specific price history. The project exposes a REST API inspired by Futbin that lets clients search players and fetch their latest prices.

## Features
- Player catalog with rating, club, nation, league, position, card type, and external IDs.
- Price snapshots per platform (PC, PlayStation, Xbox) that capture minimum, maximum, and average prices over time.
- REST API endpoints to list/search players and retrieve player details including the latest price snapshot for each platform.
- PostgreSQL-ready schema with distinct-on queries for fetching recent platform prices, and a SQLite fallback for quick local development.

## Getting Started
1. Ensure dependencies are installed:
   ```bash
   pip install -r requirements.txt
   ```
2. Configure the database (PostgreSQL recommended). Set `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, and `POSTGRES_PORT` environment variables. If these are absent, the project defaults to SQLite for convenience.
3. Apply migrations (required to create auth/session tables and app models):
   ```bash
   python manage.py migrate
   ```
4. Run the development server:
   ```bash
   python manage.py runserver
   ```

## API
- `GET /api/codex/players/` — list players with search on `name`, `club`, `nation`, and `card_type`.
- `GET /api/codex/players/<id>/` — player detail including latest price snapshots per platform.

Players are ordered alphabetically by default, and price snapshots are ordered by newest timestamp while using PostgreSQL's `DISTINCT ON` to keep only the latest per platform.

### Example Player Response
```json
{
  "id": 1,
  "name": "Ada Lovelace",
  "rating": 91,
  "club": "Mathematicians FC",
  "nation": "United Kingdom",
  "league": "Legends League",
  "position": "CAM",
  "card_type": "special",
  "external_id": "123456",
  "latest_prices": [
    {
      "platform": "pc",
      "min_price": 75000,
      "max_price": 82000,
      "average_price": 78500,
      "timestamp": "2024-09-20T15:30:00Z"
    },
    {
      "platform": "ps",
      "min_price": 74000,
      "max_price": 81000,
      "average_price": 77000,
      "timestamp": "2024-09-20T15:28:00Z"
    },
    {
      "platform": "xbox",
      "min_price": 76000,
      "max_price": 83000,
      "average_price": 79000,
      "timestamp": "2024-09-20T15:27:00Z"
    }
  ]
}
```

## Next Steps
- Add a management command to pull fresh prices from an external API.
- Build a simple search UI using Django templates.
- Render price history graphs with Chart.js.
