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
                attrs={"class": "input", "placeholder": "2900000"}
            ),
            "is_capital": forms.CheckboxInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # IntegerField.widget_attrs() min="0" qo'yadi, model esa 1 dan boshlanadi.
        # Brauzer validatsiyasi server bilan mos bo'lishi uchun to'g'rilaymiz.
        self.fields["population"].widget.attrs["min"] = 1
        self.fields["country"].empty_label = "— Mamlakatni tanlang —"

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
