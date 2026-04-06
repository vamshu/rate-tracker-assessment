from django.urls import path
from .views import latest_rates, rate_history, ingest_rate

urlpatterns = [
    path("latest", latest_rates, name="latest"),
    path("history", rate_history, name="history"),
    path("ingest/", ingest_rate)
]