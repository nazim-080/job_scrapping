from django import forms

from .models import City, Language


class FindForm(forms.Form):
    city = forms.ModelChoiceField(queryset=City.objects.all(), label='Город', to_field_name='slug', required=False)
    language = forms.ModelChoiceField(queryset=Language.objects.all(), label='Специальность',
                                      to_field_name='slug', required=False)
