from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Rate
from .serializers import RateSerializer
from django.db.models import Max
from django.core.cache import cache

@api_view(["GET"])
def latest_rates(request):
    page = int(request.GET.get("page", 1))
    limit = int(request.GET.get("limit", 10))

    cache_key = f"latest_rates_{page}_{limit}"

    cached_data = cache.get(cache_key)
    if cached_data:
        return Response(cached_data)

    latest_records = (
        Rate.objects.values("provider", "rate_type")
        .annotate(latest_date=Max("effective_date"))
    )

    result = []

    for item in latest_records:
        rate = Rate.objects.filter(
            provider=item["provider"],
            rate_type=item["rate_type"],
            effective_date=item["latest_date"],
        ).first()

        if rate:
            result.append(rate)

    start = (page - 1) * limit
    end = start + limit

    total_count = len(result)
    paginated_result = result[start:end]

    serializer = RateSerializer(paginated_result, many=True)

    response_data = {
        "results": serializer.data,
        "total": total_count,
        "page": page,
        "limit": limit,
        "pages": (total_count + limit - 1) // limit
    }

    cache.set(cache_key, response_data, timeout=60)

    return Response(response_data)


@api_view(["GET"])
def rate_history(request):
    provider = request.GET.get("provider")
    search = request.GET.get("search", "")
    page = int(request.GET.get("page", 1))
    limit = int(request.GET.get("limit", 10))

    qs = Rate.objects.all().order_by("-effective_date")

    if provider:
        qs = qs.filter(provider=provider)
    
    if search:
        qs = qs.filter(provider__icontains=search) | qs.filter(rate_type__icontains=search)

    total_count = qs.count()
    start = (page - 1) * limit
    end = start + limit

    qs_paginated = qs[start:end]

    serializer = RateSerializer(qs_paginated, many=True)
    return Response({
        "results": serializer.data,
        "total": total_count,
        "page": page,
        "limit": limit,
        "pages": (total_count + limit - 1) // limit
    })

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def ingest_rate(request):
    serializer = RateSerializer(data=request.data)

    if serializer.is_valid():
        unique_fields = {
            'provider': serializer.validated_data['provider'],
            'rate_type': serializer.validated_data['rate_type'],
            'effective_date': serializer.validated_data['effective_date'],
            'raw_response_id': serializer.validated_data['raw_response_id'],
        }
        
        update_fields = {k: v for k, v in serializer.validated_data.items() 
                        if k not in unique_fields}
        
        rate, created = Rate.objects.update_or_create(
            defaults=update_fields,
            **unique_fields
        )
        
        try:
            cache.delete_pattern("latest_rates_*")
        except (AttributeError, NotImplementedError):
            try:
                from django_redis import get_redis_connection
                redis_conn = get_redis_connection("default")
                keys = redis_conn.keys("latest_rates_*")
                if keys:
                    redis_conn.delete(*keys)
            except Exception:
                pass
        
        response_serializer = RateSerializer(rate)
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(response_serializer.data, status=status_code)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)