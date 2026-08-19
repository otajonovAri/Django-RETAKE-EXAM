from django.test import TestCase
from django.urls import reverse

from .models import City, Country


class CityCrudTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.uz = Country.objects.create(name="O'zbekiston", code="UZ")
        cls.jp = Country.objects.create(name="Yaponiya", code="JP")
        cls.tashkent = City.objects.create(
            name="Toshkent", population=2_900_000, country=cls.uz, is_capital=True
        )
        cls.tokyo = City.objects.create(
            name="Tokio", population=13_960_000, country=cls.jp, is_capital=True
        )

    def test_list_shows_all_cities(self):
        response = self.client.get(reverse("cities:list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toshkent")
        self.assertContains(response, "Tokio")
        self.assertEqual(response.context["total_cities"], 2)

    def test_filter_by_country(self):
        response = self.client.get(reverse("cities:list"), {"country": self.uz.pk})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toshkent")
        self.assertNotContains(response, "Tokio")
        self.assertEqual(response.context["total_cities"], 1)

    def test_search_by_name(self):
        response = self.client.get(reverse("cities:list"), {"q": "tok"})
        self.assertEqual(response.context["total_cities"], 1)
        self.assertContains(response, "Tokio")

    def test_sort_by_population_desc(self):
        response = self.client.get(reverse("cities:list"), {"sort": "-population"})
        cities = list(response.context["cities"])
        self.assertEqual(cities[0], self.tokyo)

    def test_create_city(self):
        response = self.client.post(
            reverse("cities:create"),
            {
                "name": "Samarqand",
                "country": self.uz.pk,
                "population": 570_000,
                "is_capital": False,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(City.objects.filter(name="Samarqand").exists())

    def test_create_duplicate_city_in_same_country_is_rejected(self):
        response = self.client.post(
            reverse("cities:create"),
            {
                "name": "toshkent",
                "country": self.uz.pk,
                "population": 100,
                "is_capital": False,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(City.objects.filter(country=self.uz).count(), 1)

    def test_update_city(self):
        response = self.client.post(
            reverse("cities:update", args=[self.tashkent.pk]),
            {
                "name": "Toshkent",
                "country": self.uz.pk,
                "population": 3_000_000,
                "is_capital": True,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.tashkent.refresh_from_db()
        self.assertEqual(self.tashkent.population, 3_000_000)

    def test_delete_city(self):
        response = self.client.post(reverse("cities:delete", args=[self.tokyo.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(City.objects.filter(pk=self.tokyo.pk).exists())

    def test_detail_page(self):
        response = self.client.get(reverse("cities:detail", args=[self.tashkent.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toshkent")


class CountryViewTests(TestCase):
    def test_country_list_reports_counts(self):
        uz = Country.objects.create(name="O'zbekiston", code="UZ")
        City.objects.create(name="Toshkent", population=2_900_000, country=uz)
        City.objects.create(name="Samarqand", population=570_000, country=uz)

        response = self.client.get(reverse("cities:country_list"))
        self.assertEqual(response.status_code, 200)
        country = response.context["countries"][0]
        self.assertEqual(country.city_count, 2)
        self.assertEqual(country.population_sum, 3_470_000)

    def test_create_country(self):
        response = self.client.post(
            reverse("cities:country_create"), {"name": "Italiya", "code": "it"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Country.objects.get(name="Italiya").code, "IT")


class CityModelTests(TestCase):
    def test_str_representation(self):
        uz = Country.objects.create(name="O'zbekiston")
        city = City.objects.create(name="Buxoro", population=280_000, country=uz)
        self.assertEqual(str(city), "Buxoro (O'zbekiston)")

    def test_deleting_country_deletes_its_cities(self):
        uz = Country.objects.create(name="O'zbekiston")
        City.objects.create(name="Xiva", population=93_000, country=uz)
        uz.delete()
        self.assertEqual(City.objects.count(), 0)


class AccessibilityTests(TestCase):
    """WCAG 2.1 AA bo'yicha tuzatilgan joylar regressiyaga uchramasligi uchun."""

    @classmethod
    def setUpTestData(cls):
        cls.uz = Country.objects.create(name="O'zbekiston", code="UZ")
        cls.city = City.objects.create(
            name="Toshkent", population=2_900_000, country=cls.uz, is_capital=True
        )

    def test_page_declares_language(self):
        html = self.client.get(reverse("cities:list")).content.decode()
        self.assertIn('<html lang="uz"', html)

    def test_skip_link_is_first_focusable_and_targets_main(self):
        html = self.client.get(reverse("cities:list")).content.decode()
        self.assertIn('class="skip-link" href="#main"', html)
        self.assertIn('id="main"', html)

    def test_nav_has_accessible_name_and_current_page(self):
        html = self.client.get(reverse("cities:list")).content.decode()
        self.assertIn('aria-label="Asosiy menyu"', html)
        self.assertIn('aria-current="page"', html)

    def test_messages_are_in_live_region(self):
        html = self.client.get(reverse("cities:list")).content.decode()
        self.assertIn('role="status"', html)
        self.assertIn('aria-live="polite"', html)

    def test_country_filter_does_not_auto_submit(self):
        """3.2.2 - tanlash o'zi sahifani yubormasligi kerak."""
        html = self.client.get(reverse("cities:list")).content.decode()
        self.assertNotIn("this.form.submit()", html)
        self.assertNotIn("onchange", html)

    def test_sortable_headers_expose_aria_sort(self):
        html = self.client.get(reverse("cities:list"), {"sort": "-population"}).content.decode()
        self.assertIn('aria-sort="descending"', html)
        self.assertIn('aria-sort="none"', html)

    def test_table_has_caption_and_row_headers(self):
        html = self.client.get(reverse("cities:list")).content.decode()
        self.assertIn("<caption>", html)
        self.assertIn('<th scope="col"', html)
        self.assertIn('<th scope="row"', html)

    def test_row_action_links_have_unique_accessible_names(self):
        html = self.client.get(reverse("cities:list")).content.decode()
        self.assertIn('<span class="visually-hidden">: Toshkent</span>', html)

    def test_invalid_field_is_marked_and_described(self):
        """3.3.1 / 4.1.2 - xato maydon aria orqali bog'lanadi."""
        response = self.client.post(
            reverse("cities:create"),
            {"name": "", "country": self.uz.pk, "population": ""},
        )
        html = response.content.decode()
        self.assertEqual(response.status_code, 200)
        self.assertIn('aria-invalid="true"', html)
        self.assertIn('aria-describedby="id_name_error"', html)
        self.assertIn('id="id_name_error"', html)
        self.assertIn('role="alert"', html)

    def test_required_fields_expose_required_attribute(self):
        html = self.client.get(reverse("cities:create")).content.decode()
        self.assertIn("required", html)
        self.assertIn("(majburiy maydon)", html)

    def test_help_text_is_associated_with_input(self):
        html = self.client.get(reverse("cities:create")).content.decode()
        self.assertIn('aria-describedby="id_population_helptext"', html)
        self.assertIn('id="id_population_helptext"', html)

    def test_population_min_matches_server_validation(self):
        html = self.client.get(reverse("cities:create")).content.decode()
        self.assertIn('min="1"', html)

    def test_pagination_nav_is_labelled(self):
        for i in range(20):
            City.objects.create(name=f"Shahar {i}", population=1000 + i, country=self.uz)
        html = self.client.get(reverse("cities:list")).content.decode()
        self.assertIn('aria-label="Sahifalar"', html)
