from django.contrib import admin

from .models import City, Country


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "city_count")
    search_fields = ("name", "code")
    ordering = ("name",)

    @admin.display(description="Shaharlar soni")
    def city_count(self, obj):
        return obj.cities.count()


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "population", "is_capital", "created_at")
    list_filter = ("country", "is_capital")
    search_fields = ("name", "country__name")
    autocomplete_fields = ("country",)
    list_select_related = ("country",)
    ordering = ("country__name", "name")
