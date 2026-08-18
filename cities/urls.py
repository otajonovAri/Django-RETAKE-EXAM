from django.urls import path

from . import views

app_name = "cities"

urlpatterns = [
    path("", views.CityListView.as_view(), name="list"),
    path("shahar/qoshish/", views.CityCreateView.as_view(), name="create"),
    path("shahar/<int:pk>/", views.CityDetailView.as_view(), name="detail"),
    path("shahar/<int:pk>/tahrirlash/", views.CityUpdateView.as_view(), name="update"),
    path("shahar/<int:pk>/ochirish/", views.CityDeleteView.as_view(), name="delete"),
    path("mamlakatlar/", views.CountryListView.as_view(), name="country_list"),
    path(
        "mamlakatlar/qoshish/",
        views.CountryCreateView.as_view(),
        name="country_create",
    ),
]
