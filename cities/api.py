"""REST API — shaharlar va mamlakatlar uchun.

O'qish (GET) hamma uchun ochiq, o'zgartirish uchun tizimga kirgan va
tegishli ruxsatga ega foydalanuvchi kerak (`DjangoModelPermissionsOrAnonReadOnly`).
"""

from django.db.models import Count, Sum
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import City, Country
from .serializers import CitySerializer, CountrySerializer


@extend_schema_view(
    list=extend_schema(
        summary="Shaharlar ro'yxati",
        description=(
            "Mamlakat bo'yicha filtrlash: `?country=<id>`. "
            "Qidiruv: `?search=Tosh`. Saralash: `?ordering=-population`."
        ),
        parameters=[
            OpenApiParameter(
                "country",
                int,
                description="Mamlakat ID'si bo'yicha filtr",
            ),
            OpenApiParameter(
                "is_capital",
                bool,
                description="Faqat poytaxtlar (`true`) yoki oddiy shaharlar (`false`)",
            ),
        ],
    ),
    retrieve=extend_schema(summary="Bitta shahar"),
    create=extend_schema(summary="Yangi shahar qo'shish"),
    update=extend_schema(summary="Shaharni to'liq yangilash"),
    partial_update=extend_schema(summary="Shaharni qisman yangilash"),
    destroy=extend_schema(summary="Shaharni o'chirish"),
)
class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.select_related("country").all()
    serializer_class = CitySerializer
    filterset_fields = ["country", "is_capital"]
    search_fields = ["name", "country__name"]
    ordering_fields = ["name", "population", "country__name", "created_at"]
    ordering = ["country__name", "name"]


@extend_schema_view(
    list=extend_schema(summary="Mamlakatlar ro'yxati (shahar soni bilan)"),
    retrieve=extend_schema(summary="Bitta mamlakat"),
    create=extend_schema(summary="Yangi mamlakat qo'shish"),
    update=extend_schema(summary="Mamlakatni to'liq yangilash"),
    partial_update=extend_schema(summary="Mamlakatni qisman yangilash"),
    destroy=extend_schema(
        summary="Mamlakatni o'chirish",
        description="Diqqat: mamlakat bilan birga uning barcha shaharlari ham o'chadi.",
    ),
)
class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.annotate(
        city_count=Count("cities"),
        population_sum=Sum("cities__population"),
    ).order_by("name")
    serializer_class = CountrySerializer
    search_fields = ["name", "code"]
    ordering_fields = ["name", "city_count", "population_sum"]

    @extend_schema(
        summary="Mamlakatning shaharlari",
        responses=CitySerializer(many=True),
    )
    @action(detail=True, methods=["get"])
    def cities(self, request, pk=None):
        """`/api/countries/<id>/cities/` — shu mamlakatdagi shaharlar."""
        country = self.get_object()
        queryset = country.cities.select_related("country").order_by("-population")

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = CitySerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(CitySerializer(queryset, many=True).data)
