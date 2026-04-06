# Database Schema

## Overview

The system uses a single primary table `Rate` to store ingested financial rate data.

---

## Table: Rate

| Field           | Type     | Description                            |
| --------------- | -------- | -------------------------------------- |
| provider        | string   | Name of the financial provider         |
| rate_type       | string   | Type of rate (e.g., mortgage, savings) |
| rate_value      | float    | Interest rate value                    |
| effective_date  | date     | Date the rate is effective             |
| ingestion_ts    | datetime | Timestamp when data was ingested       |
| source_url      | string   | Source of the data                     |
| raw_response_id | string   | Unique identifier for raw data         |
| currency        | string   | Currency code                          |

---

## Indexing Strategy

* Composite index on `(provider, rate_type, effective_date)`
  → Optimizes latest rate queries

* Index on `ingestion_ts`
  → Efficient filtering for ingestion windows

---

## Query Optimization

### 1. Latest rate per provider

* Uses aggregation (`MAX(effective_date)`) grouped by provider + rate_type
* Index helps reduce scan time

### 2. Rate change over 30 days

* Filter on `effective_date >= now() - 30 days`
* Efficient due to date-based filtering

### 3. Records in 24-hour window

* Filter using `ingestion_ts`
* Indexed for fast lookup

---

## Design Decisions

* Chose a single denormalized table to simplify queries and reduce joins
* Avoided normalization (separate provider table) to improve read performance
* Used bulk inserts for efficient ingestion of large datasets

---

## Tradeoffs

* Denormalization increases storage redundancy but improves read speed
* Lack of foreign keys reduces strict constraints but simplifies ingestion
* Limited indexing to essential queries to avoid write overhead
