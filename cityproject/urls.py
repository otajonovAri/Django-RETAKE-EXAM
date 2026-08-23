from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework.routers import DefaultRouter

from cities.api import CityViewSet, CountryViewSet

router = DefaultRouter()
router.register("cities", CityViewSet, basename="city")
router.register("countries", CountryViewSet, basename="country")

urlpatterns = [
    path("admin/", admin.site.urls),

    # REST API
    path("api/", include(router.urls)),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    # DRF brauzer interfeysi uchun kirish/chiqish
    path("api-auth/", include("rest_framework.urls")),

    # Veb interfeys
    path("", include("cities.urls")),
]

# Maxsus xato sahifalari (DEBUG=False bo'lganda ishlaydi).
handler404 = "cities.views.error_404"
handler500 = "cities.views.error_500"
handler403 = "cities.views.error_403"
