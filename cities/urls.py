from django.urls import path

from . import views

app_name = "cities"

urlpatterns = [
    # --- Shaharlar ---
    path("", views.CityListView.as_view(), name="list"),
    path("shahar/qoshish/", views.CityCreateView.as_view(), name="create"),
    path("shahar/<int:pk>/", views.CityDetailView.as_view(), name="detail"),
    path("shahar/<int:pk>/tahrirlash/", views.CityUpdateView.as_view(), name="update"),
    path("shahar/<int:pk>/ochirish/", views.CityDeleteView.as_view(), name="delete"),

    # --- Eksport (joriy filtr saqlanadi) ---
    path("eksport/csv/", views.export_cities_csv, name="export_csv"),
    path("eksport/excel/", views.export_cities_xlsx, name="export_xlsx"),

    # --- Mamlakatlar ---
    path("mamlakatlar/", views.CountryListView.as_view(), name="country_list"),
    path(
        "mamlakatlar/qoshish/",
        views.CountryCreateView.as_view(),
        name="country_create",
    ),
    path(
        "mamlakatlar/<int:pk>/",
        views.CountryDetailView.as_view(),
        name="country_detail",
    ),
    path(
        "mamlakatlar/<int:pk>/tahrirlash/",
        views.CountryUpdateView.as_view(),
        name="country_update",
    ),
    path(
        "mamlakatlar/<int:pk>/ochirish/",
        views.CountryDeleteView.as_view(),
        name="country_delete",
    ),
]
