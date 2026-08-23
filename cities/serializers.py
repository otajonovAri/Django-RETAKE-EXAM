from rest_framework import serializers

from .models import City, Country


class CountrySerializer(serializers.ModelSerializer):
    city_count = serializers.IntegerField(read_only=True)
    population_sum = serializers.IntegerField(read_only=True)

    class Meta:
        model = Country
        fields = ["id", "name", "code", "city_count", "population_sum"]

    def validate_code(self, value):
        return value.strip().upper()

    def validate_name(self, value):
        return value.strip()


class CitySerializer(serializers.ModelSerializer):
    # Yozishda mamlakat id bilan beriladi, o'qishda nomi ham qaytadi.
    country_name = serializers.CharField(source="country.name", read_only=True)
    country_code = serializers.CharField(source="country.code", read_only=True)

    class Meta:
        model = City
        fields = [
            "id",
            "name",
            "population",
            "country",
            "country_name",
            "country_code",
            "is_capital",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

    def validate_name(self, value):
        return value.strip()

    def validate(self, attrs):
        """Bitta mamlakat ichida shahar nomi takrorlanmasligini tekshiradi."""
        name = attrs.get("name", getattr(self.instance, "name", None))
        country = attrs.get("country", getattr(self.instance, "country", None))

        if name and country:
            duplicate = City.objects.filter(name__iexact=name, country=country)
            if self.instance is not None:
                duplicate = duplicate.exclude(pk=self.instance.pk)
            if duplicate.exists():
                raise serializers.ValidationError(
                    {
                        "name": (
                            f"{country.name} mamlakatida «{name}» shahri "
                            "allaqachon mavjud."
                        )
                    }
                )
        return attrs
