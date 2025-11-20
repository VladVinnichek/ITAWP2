from django import forms
from .models import Product, Category, ProductAttribute

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'sku', 'price', 'category', 'status', 'rating', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название продукта'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Введите описание продукта'}),
            'sku': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите артикул'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0', 'max': '5'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'name': 'Название продукта',
            'description': 'Описание',
            'sku': 'Артикул (SKU)',
            'price': 'Цена',
            'category': 'Категория',
            'status': 'Статус',
            'rating': 'Рейтинг',
            'is_active': 'Активный',
        }

class ProductAttributeForm(forms.ModelForm):
    class Meta:
        model = ProductAttribute
        fields = ['attribute_type', 'value', 'display_order']