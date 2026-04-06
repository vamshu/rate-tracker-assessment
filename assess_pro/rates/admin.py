from django.contrib import admin
from .models import Rate

@admin.register(Rate)
class RateAdmin(admin.ModelAdmin):
    list_display = ('provider', 'rate_type', 'rate_value', 'currency', 'effective_date', 'ingested_at')
    search_fields = ('provider', 'rate_type', 'currency')
    list_filter = ('provider', 'rate_type', 'currency', 'effective_date')
    readonly_fields = ('ingested_at',)
