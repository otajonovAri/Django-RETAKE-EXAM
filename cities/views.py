from django.contrib import messages
from django.db.models import Count, Q, Sum
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import CityForm, CountryForm
from .models import City, Country

SORT_FIELDS = {
    "name": "name",
    "-name": "-name",
    "population": "population",
    "-population": "-population",
    "country": "country__name",
    "-country": "-country__name",
}

# Jadval sarlavhalari: (kalit, ko'rinadigan nom, raqamli ustunmi)
SORTABLE_COLUMNS = (
    ("name", "Shahar nomi", False),
    ("country", "Mamlakat", False),
    ("population", "Aholisi", True),
)


class CityListView(ListView):
    """Shaharlar ro'yxati - jadval ko'rinishida, mamlakat bo'yicha filtrlanadi."""

    model = City
    template_name = "cities/city_list.html"
    context_object_name = "cities"
    paginate_by = 15

    def get_queryset(self):
        queryset = City.objects.select_related("country")

        country_id = self.request.GET.get("country")
        if country_id and country_id.isdigit():
            queryset = queryset.filter(country_id=int(country_id))

        query = self.request.GET.get("q", "").strip()
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(country__name__icontains=query)
            )

        sort = self.request.GET.get("sort", "")
        if sort in SORT_FIELDS:
            queryset = queryset.order_by(SORT_FIELDS[sort])

        return queryset

    def _sort_headers(self, sort, base_params):
        """Har bir ustun uchun aria-sort holati va keyingi saralash havolasi."""
        headers = []
        for key, label, numeric in SORTABLE_COLUMNS:
            ascending = sort == key
            descending = sort == f"-{key}"

            if numeric:
                next_sort = key if descending else f"-{key}"
            else:
                next_sort = f"-{key}" if ascending else key

            params = base_params.copy()
            params["sort"] = next_sort

            direction = "kamayish" if next_sort.startswith("-") else "o'sish"

            headers.append({
                "key": key,
                "label": label,
                "numeric": numeric,
                "aria_sort": (
                    "ascending" if ascending
                    else "descending" if descending
                    else "none"
                ),
                "url": f"?{params.urlencode()}",
                "action": f"{label} bo'yicha {direction} tartibida saralash",
            })
        return headers

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filtered = self.get_queryset()

        selected_country = self.request.GET.get("country", "")
        query = self.request.GET.get("q", "")
        sort = self.request.GET.get("sort", "")

        # Sahifalash va saralash havolalarida filtr yo'qolmasligi uchun.
        base_params = self.request.GET.copy()
        base_params.pop("page", None)
        base_params.pop("sort", None)

        page_params = self.request.GET.copy()
        page_params.pop("page", None)

        context.update({
            "nav_section": "cities",
            "countries": Country.objects.annotate(
                city_count=Count("cities")
            ).order_by("name"),
            "selected_country": selected_country,
            "query": query,
            "sort": sort,
            "total_cities": filtered.count(),
            "total_population": filtered.aggregate(total=Sum("population"))["total"] or 0,
            "is_filtered": bool(selected_country or query),
            "querystring": page_params.urlencode(),
            "sort_headers": self._sort_headers(sort, base_params),
        })
        return context


class CityDetailView(DetailView):
    model = City
    template_name = "cities/city_detail.html"
    context_object_name = "city"
    queryset = City.objects.select_related("country")
    extra_context = {"nav_section": "cities"}


class CityCreateView(CreateView):
    model = City
    form_class = CityForm
    template_name = "cities/city_form.html"
    extra_context = {
        "title": "Yangi shahar qo'shish",
        "submit_label": "Qo'shish",
        "nav_section": "cities",
    }

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"«{self.object.name}» shahri qo'shildi.")
        return response


class CityUpdateView(UpdateView):
    model = City
    form_class = CityForm
    template_name = "cities/city_form.html"
    extra_context = {
        "title": "Shaharni tahrirlash",
        "submit_label": "Saqlash",
        "nav_section": "cities",
    }

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"«{self.object.name}» ma'lumotlari yangilandi.")
        return response


class CityDeleteView(DeleteView):
    model = City
    template_name = "cities/city_confirm_delete.html"
    success_url = reverse_lazy("cities:list")
    context_object_name = "city"
    extra_context = {"nav_section": "cities"}

    def form_valid(self, form):
        messages.success(self.request, f"«{self.object.name}» shahri o'chirildi.")
        return super().form_valid(form)


class CountryListView(ListView):
    """Mamlakatlar kesimidagi statistika."""

    model = Country
    template_name = "cities/country_list.html"
    context_object_name = "countries"
    extra_context = {"nav_section": "countries"}

    def get_queryset(self):
        return Country.objects.annotate(
            city_count=Count("cities"),
            population_sum=Sum("cities__population"),
        ).order_by("-city_count", "name")


class CountryCreateView(CreateView):
    model = Country
    form_class = CountryForm
    template_name = "cities/country_form.html"
    success_url = reverse_lazy("cities:country_list")
    extra_context = {"nav_section": "countries"}

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"«{self.object.name}» mamlakati qo'shildi.")
        return response
