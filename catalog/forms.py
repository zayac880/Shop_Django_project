from django import forms
from django.forms import BaseInlineFormSet

from catalog.models import Product, Version


class StyleForm:
    """
    Базовый класс для форм с применением стиля.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'is_current_version':
                continue
            field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleForm, forms.ModelForm):
    """
    Форма для создания/редактирования продукта.
    """
    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'category', 'image')

    def clean_name(self):
        """
        Проверка на запрещенные слова в наименовании продукта.
        """
        cleaned_data = self.cleaned_data.get('name')
        words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
        for word in words:
            if word in cleaned_data:
                raise forms.ValidationError('Вы вели запрещенное слово в наименовании')
        return cleaned_data

    def clean_description(self):
        """
        Проверка на запрещенные слова в описании продукта.
        """
        cleaned_data = self.cleaned_data.get('description')
        words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
        for word in words:
            if word in cleaned_data:
                raise forms.ValidationError('Вы вели запрещенное слово в описании')
        return cleaned_data


class VersionForm(StyleForm, forms.ModelForm):
    """
    Форма для создания/редактирования версии продукта.
    """
    class Meta:
        model = Version
        fields = '__all__'


class VersionFormSet(BaseInlineFormSet):
    """
    Формсет для версий продукта.
    """
    def clean(self):
        """
        Проверка на активность более одной версии.
        """
        super().clean()
        cont_cur_version = 0
        for form in self.forms:
            if form['is_current_version'].data:
                cont_cur_version += 1
        if cont_cur_version > 1:
            raise forms.ValidationError('Только одна версия может быть активной')
