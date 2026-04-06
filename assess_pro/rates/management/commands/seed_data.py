import pandas as pd
from django.core.management.base import BaseCommand
from rates.models import Rate
from django.utils.timezone import make_aware
from datetime import datetime


class Command(BaseCommand):
    def handle(self, *args, **kwargs):

        # Load only first 50k rows
        df = pd.read_parquet("/app/rates_seed.parquet").head(50000)

        print(f"Loaded rows: {len(df)}")

        objs = []
        count = 0

        for row in df.itertuples(index=False):
            try:
                ingestion_ts = getattr(row, "ingestion_ts", None)

                if pd.notna(ingestion_ts):
                    if isinstance(ingestion_ts, datetime) and ingestion_ts.tzinfo is None:
                        ingestion_ts = make_aware(ingestion_ts)
                else:
                    continue

                objs.append(
                    Rate(
                        provider=getattr(row, "provider", ""),
                        rate_type=getattr(row, "rate_type", ""),
                        rate_value=getattr(row, "rate_value", 0),
                        effective_date=getattr(row, "effective_date"),
                        ingestion_ts=ingestion_ts,
                        source_url=getattr(row, "source_url", ""),
                        raw_response_id=getattr(row, "raw_response_id", ""),
                        currency=getattr(row, "currency", ""),
                    )
                )

                count += 1

                if count % 5000 == 0:
                    print(f"Processed {count} rows...")

            except Exception as e:
                print("--Skipping row:", e)

        print(" Inserting into DB in batches...")

        batch_size = 5000
        for i in range(0, len(objs), batch_size):
            Rate.objects.bulk_create(
                objs[i:i + batch_size],
                ignore_conflicts=True
            )
            print(f"Inserted {i + batch_size} records...")

        print(f"Done! Inserted {len(objs)} records")