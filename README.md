# Rate Tracker Dashboard

## Overview

This project ingests rate data from a parquet file, stores it in PostgreSQL, and displays the latest rates via a Next.js dashboard.

## Tech Stack

* Backend: Django + Django REST Framework
* Frontend: Next.js
* Database: PostgreSQL
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
* Backend API: http://localhost:8000/api/rates/history

## Features

* Load data from parquet file
* Optimized bulk ingestion (50k rows)
* Latest rates API
* Historical rates API
* Auto-refresh dashboard (60s)
* Provider filtering

## Performance

* Used `bulk_create` for fast inserts
* Limited dataset to 50k for local performance

## AI Usage

Used ChatGPT for:

* Debugging Docker issues
* Optimizing data ingestion
* Structuring frontend integration
