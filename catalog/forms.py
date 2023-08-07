from django import forms

from catalog.models import Product, Version


class StyleForm:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleForm, forms.ModelForm):

    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'category', 'image')

    def clean_name(self):
        cleaned_data = self.cleaned_data.get('name')
        words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
        for word in words:
            if word in cleaned_data:
                raise forms.ValidationError('Вы вели запрещенное слово в наименовании')
        return cleaned_data

    def clean_description(self):
        cleaned_data = self.cleaned_data.get('description')
        words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
        for word in words:
            if word in cleaned_data:
                raise forms.ValidationError('Вы вели запрещенное слово в описании')
        return cleaned_data


class VersionForm(StyleForm, forms.ModelForm):

    class Meta:
        model = Version
        fields = '__all__'
