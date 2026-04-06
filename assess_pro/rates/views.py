from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Rate
from .serializers import RateSerializer
from django.db.models import Max

@api_view(["GET"])
def latest_rates(request):
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

    page = int(request.GET.get("page", 1))
    limit = int(request.GET.get("limit", 10))
    start = (page - 1) * limit
    end = start + limit

    total_count = len(result)
    paginated_result = result[start:end]

    serializer = RateSerializer(paginated_result, many=True)
    return Response({
        "results": serializer.data,
        "total": total_count,
        "page": page,
        "limit": limit,
        "pages": (total_count + limit - 1) // limit
    })


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
