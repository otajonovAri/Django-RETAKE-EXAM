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


class CityListView(ListView):
    """Shaharlar ro'yxati — jadval ko'rinishida, mamlakat bo'yicha filtrlanadi."""

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filtered = self.get_queryset()

        context["countries"] = Country.objects.annotate(
            city_count=Count("cities")
        ).order_by("name")
        context["selected_country"] = self.request.GET.get("country", "")
        context["query"] = self.request.GET.get("q", "")
        context["sort"] = self.request.GET.get("sort", "")
        context["total_cities"] = filtered.count()
        context["total_population"] = (
            filtered.aggregate(total=Sum("population"))["total"] or 0
        )
        context["is_filtered"] = bool(
            context["selected_country"] or context["query"]
        )

        # Sahifalash havolalarida filtr parametrlari yo'qolmasligi uchun.
        params = self.request.GET.copy()
        params.pop("page", None)
        context["querystring"] = params.urlencode()
        return context


class CityDetailView(DetailView):
    model = City
    template_name = "cities/city_detail.html"
    context_object_name = "city"
    queryset = City.objects.select_related("country")


class CityCreateView(CreateView):
    model = City
    form_class = CityForm
    template_name = "cities/city_form.html"
    extra_context = {"title": "Yangi shahar qo'shish", "submit_label": "Qo'shish"}

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"«{self.object.name}» shahri qo'shildi.")
        return response


class CityUpdateView(UpdateView):
    model = City
    form_class = CityForm
    template_name = "cities/city_form.html"
    extra_context = {"title": "Shaharni tahrirlash", "submit_label": "Saqlash"}

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"«{self.object.name}» ma'lumotlari yangilandi.")
        return response


class CityDeleteView(DeleteView):
    model = City
    template_name = "cities/city_confirm_delete.html"
    success_url = reverse_lazy("cities:list")
    context_object_name = "city"

    def form_valid(self, form):
        messages.success(self.request, f"«{self.object.name}» shahri o'chirildi.")
        return super().form_valid(form)


class CountryListView(ListView):
    """Mamlakatlar kesimidagi statistika."""

    model = Country
    template_name = "cities/country_list.html"
    context_object_name = "countries"

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

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"«{self.object.name}» mamlakati qo'shildi.")
        return response
