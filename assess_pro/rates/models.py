from django.db import models

class Rate(models.Model):
    provider = models.CharField(max_length=255)
    rate_type = models.CharField(max_length=100)
    rate_value = models.FloatField()
    effective_date = models.DateField()
    ingestion_ts = models.DateTimeField()
    source_url = models.URLField()
    raw_response_id = models.CharField(max_length=255)
    currency = models.CharField(max_length=10)
    ingested_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            'provider',
            'rate_type',
            'effective_date',
            'raw_response_id'
        )