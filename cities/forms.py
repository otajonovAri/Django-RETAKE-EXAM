from django import forms

from .models import City, Country


class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ["name", "country", "population", "is_capital"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "input", "placeholder": "Masalan: Toshkent"}
            ),
            "country": forms.Select(attrs={"class": "input"}),
            "population": forms.NumberInput(
                attrs={"class": "input", "min": 1, "placeholder": "2900000"}
            ),
            "is_capital": forms.CheckboxInput(attrs={"class": "checkbox"}),
        }

    def clean_name(self):
        return self.cleaned_data["name"].strip()

    def clean(self):
        cleaned = super().clean()
        name = cleaned.get("name")
        country = cleaned.get("country")
        if name and country:
            duplicate = City.objects.filter(
                name__iexact=name, country=country
            ).exclude(pk=self.instance.pk)
            if duplicate.exists():
                raise forms.ValidationError(
                    f"{country.name} mamlakatida «{name}» shahri allaqachon mavjud."
                )
        return cleaned


class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ["name", "code"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "input", "placeholder": "Masalan: O'zbekiston"}
            ),
            "code": forms.TextInput(
                attrs={"class": "input", "placeholder": "UZ", "maxlength": 3}
            ),
        }

    def clean_name(self):
        return self.cleaned_data["name"].strip()

    def clean_code(self):
        return self.cleaned_data["code"].strip().upper()
