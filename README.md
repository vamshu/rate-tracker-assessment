# Rate Tracker Dashboard

## Overview

This project ingests rate data from a parquet file, stores it in PostgreSQL, and displays the latest rates via a Next.js dashboard. The data with pagination, search, and auto-refresh.

## Tech Stack

* Backend: Django + Django REST Framework
* Frontend: Next.js
* Database: PostgreSQL
* Cache: Redis
* Containerization: Docker

## How to Run

### Prerequisites

* Docker & Docker Compose

### Run Project

```bash
docker-compose up --build
```

## Data Ingestion

The dataset is provided as a parquet file.

To load data into the database:

```bash
docker exec -it django_backend python manage.py seed_data
```

### Notes

* Only 50,000 records are ingested for performance reasons
* Bulk insert is used for efficient database writes
* The ingestion process is idempotent (safe to re-run)


### Access

* Frontend: http://localhost:3000
* Backend APIs: http://localhost:8000/api/rates/history, http://localhost:8000/api/rates/latest


### Authentication (For Ingest API)

## Create a superuser:
```bash
docker exec -it django_backend python manage.py createsuperuser
```

* Example:
Username: root

## Generate token:

```bash
docker exec -it django_backend python manage.py drf_create_token root   #username - root
```

### API Endpoints
1. GET /api/rates/latest
  * Returns latest rate per provider
  * Cached using Redis (60 seconds)
2. GET /api/rates/history
  * Paginated historical data

  ## Supports:
  * page
  * limit
  * search

3. POST /api/rates/ingest
  * Requires Bearer Token authentication
  Headers:
  Authorization: Token <your_token>
  Example Request:
  {
    "provider": "TestBank",
    "rate_type": "mortgage",
    "rate_value": 5.5,
    "effective_date": "2026-04-01",
    "ingestion_ts": "2026-04-01T10:00:00Z",
    "source_url": "https://vamshu.com",
    "raw_response_id": "abc123",
    "currency": "USD"
  }


### Features
* Parquet data ingestion
* Optimized bulk inserts
* Idempotent ingestion
* REST API with pagination
* Redis caching
* Token-based authentication
* Frontend dashboard
* Search + pagination
* Auto-refresh (60 seconds)


### Performance
* Bulk insert used for large datasets
* Dataset limited to 50K rows for local execution
* Redis caching reduces DB load

### AI Usage

Used AI tools (ChatGPT) for:

Debugging Docker issues
Optimizing ingestion performance

