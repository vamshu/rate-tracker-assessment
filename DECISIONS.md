# Engineering Decisions

## 1. Assumptions

* Data in parquet file is mostly clean but may contain null values
* Latest rate is determined by `effective_date`
* System runs in a containerized environment

## 2. Idempotency Strategy

* Used `bulk_create(ignore_conflicts=True)` to prevent duplicate inserts
* Unique combination assumed: provider + rate_type + effective_date + raw_response_id
* Safe to rerun ingestion without duplicating data

## 3. Tradeoff

* Limited ingestion to 50,000 rows instead of full dataset (~1M rows)
* Chosen to optimize local performance and avoid memory/CPU bottlenecks within 48-hour constraint

## 4. Future Improvements

* Replace polling with WebSockets for real-time updates
* Add pagination and indexing for large datasets
* Use Celery for background ingestion of full dataset
* Improve UI with charts and filtering options
