from django.core.management.base import BaseCommand
from django.db import transaction

from cities.models import City, Country

SEED_DATA = [
    ("O'zbekiston", "UZ", [
        ("Toshkent", 2_900_000, True),
        ("Samarqand", 570_000, False),
        ("Namangan", 660_000, False),
        ("Andijon", 450_000, False),
        ("Buxoro", 280_000, False),
    ]),
    ("Yaponiya", "JP", [
        ("Tokio", 13_960_000, True),
        ("Osaka", 2_690_000, False),
        ("Yokohama", 3_760_000, False),
    ]),
    ("Turkiya", "TR", [
        ("Ankara", 5_660_000, True),
        ("Istanbul", 15_520_000, False),
        ("Izmir", 4_360_000, False),
    ]),
    ("Fransiya", "FR", [
        ("Parij", 2_140_000, True),
        ("Marsel", 870_000, False),
        ("Lion", 520_000, False),
    ]),
    ("Braziliya", "BR", [
        ("Braziliya", 3_050_000, True),
        ("San-Paulu", 12_330_000, False),
        ("Rio-de-Janeyro", 6_750_000, False),
    ]),
    ("Misr", "EG", [
        ("Qohira", 9_540_000, True),
        ("Iskandariya", 5_200_000, False),
    ]),
    ("Kanada", "CA", [
        ("Ottava", 1_020_000, True),
        ("Toronto", 2_930_000, False),
        ("Vankuver", 675_000, False),
    ]),
]


class Command(BaseCommand):
    help = "Ma'lumotlar bazasini namuna shaharlar bilan to'ldiradi."

    def add_arguments(self, parser):
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Avval mavjud shahar va mamlakatlarni o'chirib tashlaydi.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options["flush"]:
            City.objects.all().delete()
            Country.objects.all().delete()
            self.stdout.write(self.style.WARNING("Eski ma'lumotlar o'chirildi."))

        created_countries = created_cities = 0

        for country_name, code, cities in SEED_DATA:
            country, was_created = Country.objects.get_or_create(
                name=country_name, defaults={"code": code}
            )
            created_countries += was_created

            for city_name, population, is_capital in cities:
                _, city_created = City.objects.get_or_create(
                    name=city_name,
                    country=country,
                    defaults={"population": population, "is_capital": is_capital},
                )
                created_cities += city_created

        self.stdout.write(
            self.style.SUCCESS(
                f"Tayyor: {created_countries} ta mamlakat, {created_cities} ta shahar qo'shildi."
            )
        )
