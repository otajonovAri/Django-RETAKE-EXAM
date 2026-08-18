from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse


class Country(models.Model):
    """Shahar tegishli bo'lgan mamlakat."""

    name = models.CharField("Mamlakat nomi", max_length=100, unique=True)
    code = models.CharField(
        "ISO kodi",
        max_length=3,
        blank=True,
        help_text="Ixtiyoriy: UZ, KZ, TR kabi qisqartma.",
    )

    class Meta:
        verbose_name = "Mamlakat"
        verbose_name_plural = "Mamlakatlar"
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def total_population(self):
        return sum(city.population for city in self.cities.all())


class City(models.Model):
    """Dunyo shaharlari ma'lumotnomasidagi bitta shahar."""

    name = models.CharField("Shahar nomi", max_length=120)
    population = models.PositiveIntegerField(
        "Aholisi",
        validators=[MinValueValidator(1)],
        help_text="Aholi soni (kishi).",
    )
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name="cities",
        verbose_name="Mamlakat",
    )
    is_capital = models.BooleanField("Poytaxtmi?", default=False)
    created_at = models.DateTimeField("Qo'shilgan sana", auto_now_add=True)
    updated_at = models.DateTimeField("O'zgartirilgan sana", auto_now=True)

    class Meta:
        verbose_name = "Shahar"
        verbose_name_plural = "Shaharlar"
        ordering = ["country__name", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["name", "country"],
                name="unique_city_per_country",
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.country.name})"

    def get_absolute_url(self):
        return reverse("cities:detail", args=[self.pk])
