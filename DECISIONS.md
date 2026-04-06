# Engineering Decisions

## 1. Assumptions

* Data in parquet file is mostly clean but may contain null values
* Latest rate is determined by `effective_date`
* System runs in a containerized environment

## 2. Idempotency Strategy

* Used `bulk_create(ignore_conflicts=True)` to prevent duplicate inserts
* Unique combination assumed: provider + rate_type + effective_date + raw_response_id
* Safe to rerun ingestion without duplicating data

## 3. Caching Strategy
* Redis used for caching /rates/latest
* Cache TTL set to 60 seconds
* Cache keys include pagination parameters
* Cache invalidated when new data is ingested via POST endpoint

## 4. Authentication Decision
* Token-based authentication used for ingest endpoint
* No external auth provider used (simplified for assessment)
* GET endpoints remain public

## 5. Tradeoff

* Limited ingestion to 50,000 rows instead of full dataset (~1M rows)
* Chosen to optimize local performance and avoid memory/CPU bottlenecks within 48-hour constraint

## 6. API Design Decisions
* /rates/latest → aggregated latest data per provider
* /rates/history → paginated to avoid large responses
* /rates/ingest → strict validation + authentication

## 7. Scheduler (Deferred)
* Ingestion currently triggered manually
* In production, would use:
    * Celery + Redis for async jobs
    * Or cron-based scheduling

## 5. Future Improvements

* Replace polling with WebSockets for real-time updates
* Add background ingestion using Celery
* Add database indexing optimization
* Implement full dataset ingestion pipeline
* Add charts in frontend for better visualization
* Improve observability with structured logging
