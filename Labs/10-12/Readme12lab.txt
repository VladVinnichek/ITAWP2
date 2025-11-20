Полная инструкция по настройке Django проекта "Product Catalog" (продолжение 11 лабораторной).

Для повторного запуска пусле перезагрузки ПК нужно запустить только Start.bat, и если нужен публичный URL: Public.bat!!!

Шаг 1: Создание структуры папок шаблонов
Создайте папку templates в приложении:
C:\Users\VladVinnichek\Desktop\BRU\ITIWP\Labs\12\product_catalog_project\product_catalog\templates\product_catalog\

Шаг 2: Создание базового шаблона
Создайте файл: C:\Users\VladVinnichek\Desktop\BRU\ITIWP\Labs\12\product_catalog_project\product_catalog\templates\product_catalog\base.html

<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Каталог продуктов{% endblock %}</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            padding-bottom: 15px;
            border-bottom: 2px solid #e74c3c;
        }
        .nav-links a {
            margin-left: 20px;
            text-decoration: none;
            color: #3498db;
            font-weight: bold;
        }
        .nav-links a:hover {
            color: #e74c3c;
        }
        .btn {
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            font-size: 14px;
        }
        .btn-primary {
            background: #3498db;
            color: white;
        }
        .btn-success {
            background: #27ae60;
            color: white;
        }
        .btn-danger {
            background: #e74c3c;
            color: white;
        }
        .btn-warning {
            background: #f39c12;
            color: white;
        }
        .product-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        .product-card {
            border: 1px solid #ddd;
            padding: 15px;
            border-radius: 8px;
            background: white;
        }
        .product-actions {
            margin-top: 15px;
            display: flex;
            gap: 10px;
        }
        .form-group {
            margin-bottom: 15px;
        }
        .form-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        .form-control {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
        }
        .attribute-badge {
            display: inline-block;
            background: #e8f4fd;
            padding: 4px 8px;
            margin: 2px;
            border-radius: 3px;
            font-size: 0.9em;
        }
        .messages {
            margin: 15px 0;
            padding: 10px;
            border-radius: 4px;
        }
        .success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛍️ Каталог продуктов</h1>
            <div class="nav-links">
                <a href="{% url 'product_list' %}">Все продукты</a>
                <a href="{% url 'product_create' %}">Добавить продукт</a>
                <a href="{% url 'category_list' %}">Категории</a>
            </div>
        </div>

        {% if messages %}
            {% for message in messages %}
                <div class="messages {{ message.tags }}">{{ message }}</div>
            {% endfor %}
        {% endif %}

        {% block content %}
        {% endblock %}
    </div>
</body>
</html>


Шаг 3: Создание forms.py
Создайте файл: C:\Users\VladVinnichek\Desktop\BRU\ITIWP\Labs\12\product_catalog_project\product_catalog\forms.py

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
		
		
Шаг 4: Обновление views.py
Замените содержимое файла: C:\Users\VladVinnichek\Desktop\BRU\ITIWP\Labs\12\product_catalog_project\product_catalog\views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.contrib import messages
from django.urls import reverse
from .models import Product, ProductAttribute, Category
from .forms import ProductForm

def product_list(request):
    products = Product.objects.filter(is_active=True).select_related('category').prefetch_related('attributes')
    return render(request, 'product_catalog/product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product.objects.prefetch_related('attributes'), pk=pk)
    return render(request, 'product_catalog/product_detail.html', {'product': product})

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Продукт "{product.name}" успешно создан!')
            return redirect('product_list')
    else:
        form = ProductForm()
    
    return render(request, 'product_catalog/product_form.html', {
        'form': form,
        'title': 'Добавление нового продукта'
    })

def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Продукт "{product.name}" успешно обновлен!')
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'product_catalog/product_form.html', {
        'form': form,
        'title': f'Редактирование продукта: {product.name}'
    })

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f'Продукт "{product_name}" успешно удален!')
        return redirect('product_list')
    
    return render(request, 'product_catalog/product_confirm_delete.html', {'product': product})

def category_list(request):
    categories = Category.objects.prefetch_related('products')
    return render(request, 'product_catalog/category_list.html', {'categories': categories})

def index(request):
    products = Product.objects.filter(is_active=True).select_related('category').prefetch_related('attributes')[:6]
    current_time = timezone.localtime(timezone.now()).strftime('%d.%m.%Y %H:%M')
    
    # Правильный подсчет продуктов в наличии
    total_products = Product.objects.filter(is_active=True).count()
    in_stock_count = Product.objects.filter(is_active=True, status='in_stock').count()
    
    return render(request, 'product_catalog/index.html', {
        'products': products,
        'current_time': current_time,
        'total_products': total_products,
        'in_stock_count': in_stock_count  # Добавляем правильный счетчик
    })
	
	
Шаг 5: Создание остальных шаблонов
product_list.html:

{% extends 'product_catalog/base.html' %}

{% block title %}Список продуктов - Каталог продуктов{% endblock %}

{% block content %}
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
    <h2>📦 Все продукты</h2>
    <a href="{% url 'product_create' %}" class="btn btn-primary">+ Добавить продукт</a>
</div>

{% if products %}
    <div class="product-grid">
        {% for product in products %}
        <div class="product-card">
            <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 10px;">
                <div>
                    <h3 style="margin: 0; color: #333;">{{ product.name }}</h3>
                    <small style="color: #666;">Артикул: {{ product.sku }}</small>
                </div>
                <div style="font-size: 1.3em; color: #e74c3c; font-weight: bold;">
                    {{ product.price }} руб.
                </div>
            </div>
            
            <p>{{ product.description|truncatewords:20 }}</p>
            
            {% if product.attributes.all %}
            <div style="margin: 10px 0;">
                {% for attr in product.attributes.all %}
                <span class="attribute-badge">
                    <strong>{{ attr.get_attribute_type_display }}:</strong> {{ attr.value }}
                </span>
                {% endfor %}
            </div>
            {% endif %}
            
            <div style="color: #666; font-size: 0.9em; margin: 10px 0;">
                <span style="color: {% if product.status == 'in_stock' %}#27ae60{% elif product.status == 'out_of_stock' %}#e67e22{% else %}#95a5a6{% endif %};">
                    📊 {{ product.get_status_display }}
                </span>
                <span style="margin-left: 15px;">⭐ {{ product.rating }}/5</span>
                {% if product.category %}
                <span style="margin-left: 15px;">📁 {{ product.category.name }}</span>
                {% endif %}
            </div>
            
            <div class="product-actions">
                <a href="{% url 'product_detail' product.id %}" class="btn btn-primary">Просмотр</a>
                <a href="{% url 'product_edit' product.id %}" class="btn btn-warning">Редактировать</a>
                <a href="{% url 'product_delete' product.id %}" class="btn btn-danger" 
                   onclick="return confirm('Вы уверены, что хотите удалить продукт {{ product.name }}?')">Удалить</a>
            </div>
        </div>
        {% endfor %}
    </div>
{% else %}
    <div style="text-align: center; padding: 40px;">
        <h3>😔 Продукты не найдены</h3>
        <p>Пока нет добавленных продуктов. <a href="{% url 'product_create' %}">Добавьте первый продукт</a>.</p>
    </div>
{% endif %}
{% endblock %}


product_form.html:

{% extends 'product_catalog/base.html' %}

{% block title %}{{ title }} - Каталог продуктов{% endblock %}

{% block content %}
<h2>{{ title }}</h2>

<form method="post">
    {% csrf_token %}
    
    <div class="form-group">
        <label for="id_name">Название продукта:</label>
        {{ form.name }}
    </div>
    
    <div class="form-group">
        <label for="id_description">Описание:</label>
        {{ form.description }}
    </div>
    
    <div class="form-group">
        <label for="id_sku">Артикул (SKU):</label>
        {{ form.sku }}
    </div>
    
    <div class="form-group">
        <label for="id_price">Цена:</label>
        {{ form.price }}
    </div>
    
    <div class="form-group">
        <label for="id_category">Категория:</label>
        {{ form.category }}
    </div>
    
    <div class="form-group">
        <label for="id_status">Статус:</label>
        {{ form.status }}
    </div>
    
    <div class="form-group">
        <label for="id_rating">Рейтинг:</label>
        {{ form.rating }}
    </div>
    
    <div class="form-group">
        <label>
            {{ form.is_active }} Активный
        </label>
    </div>
    
    <div style="display: flex; gap: 10px; margin-top: 20px;">
        <button type="submit" class="btn btn-success">Сохранить</button>
        <a href="{% url 'product_list' %}" class="btn btn-primary">Отмена</a>
    </div>
</form>
{% endblock %}


product_detail.html:

{% extends 'product_catalog/base.html' %}

{% block title %}{{ product.name }} - Каталог продуктов{% endblock %}

{% block content %}
<div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 20px;">
    <div>
        <h2>{{ product.name }}</h2>
        <p><strong>Артикул:</strong> {{ product.sku }}</p>
    </div>
    <div style="font-size: 1.5em; color: #e74c3c; font-weight: bold;">
        {{ product.price }} руб.
    </div>
</div>

<div class="form-group">
    <label><strong>Описание:</strong></label>
    <p>{{ product.description }}</p>
</div>

{% if product.attributes.all %}
<div class="form-group">
    <label><strong>Характеристики:</strong></label>
    <div>
        {% for attr in product.attributes.all %}
        <span class="attribute-badge">
            <strong>{{ attr.get_attribute_type_display }}:</strong> {{ attr.value }}
        </span>
        {% endfor %}
    </div>
</div>
{% endif %}

<div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
    <p><strong>📊 Статус:</strong> {{ product.get_status_display }}</p>
    <p><strong>⭐ Рейтинг:</strong> {{ product.rating }}/5</p>
    {% if product.category %}
    <p><strong>📁 Категория:</strong> {{ product.category.name }}</p>
    {% endif %}
    <p><strong>📅 Дата добавления:</strong> {{ product.created_at|date:"d.m.Y H:i" }}</p>
    <p><strong>🔄 Последнее обновление:</strong> {{ product.updated_at|date:"d.m.Y H:i" }}</p>
</div>

<div style="display: flex; gap: 10px; margin-top: 20px;">
    <a href="{% url 'product_edit' product.id %}" class="btn btn-warning">Редактировать</a>
    <a href="{% url 'product_delete' product.id %}" class="btn btn-danger" 
       onclick="return confirm('Вы уверены, что хотите удалить продукт {{ product.name }}?')">Удалить</a>
    <a href="{% url 'product_list' %}" class="btn btn-primary">Назад к списку</a>
</div>
{% endblock %}


product_confirm_delete.html:

{% extends 'product_catalog/base.html' %}

{% block title %}Удаление продукта - Каталог продуктов{% endblock %}

{% block content %}
<h2>❌ Удаление продукта</h2>

<div style="background: #f8d7da; padding: 15px; border-radius: 5px; margin: 20px 0;">
    <h3 style="color: #721c24; margin: 0;">Внимание!</h3>
    <p style="color: #721c24; margin: 10px 0 0 0;">
        Вы собираетесь удалить продукт <strong>"{{ product.name }}"</strong> (артикул: {{ product.sku }}).
        Это действие нельзя отменить.
    </p>
</div>

<form method="post">
    {% csrf_token %}
    <div style="display: flex; gap: 10px;">
        <button type="submit" class="btn btn-danger">Да, удалить</button>
        <a href="{% url 'product_list' %}" class="btn btn-primary">Отмена</a>
    </div>
</form>
{% endblock %}


index.html:

{% extends 'product_catalog/base.html' %}

{% block title %}Главная - Каталог продуктов{% endblock %}

{% block content %}
<h2>🛍️ Добро пожаловать в каталог продуктов</h2>
<p><strong>Время:</strong> {{ current_time }}</p>

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 30px 0;">
    <div style="background: #e8f4fd; padding: 20px; border-radius: 8px; text-align: center;">
        <h3 style="margin: 0; color: #3498db;">📦</h3>
        <h4 style="margin: 10px 0;">Всего продуктов</h4>
        <p style="font-size: 2em; font-weight: bold; margin: 0; color: #3498db;">{{ total_products }}</p>
    </div>
    <div style="background: #e8f6f3; padding: 20px; border-radius: 8px; text-align: center;">
        <h3 style="margin: 0; color: #27ae60;">🛒</h3>
        <h4 style="margin: 10px 0;">В наличии</h4>
        <p style="font-size: 2em; font-weight: bold; margin: 0; color: #27ae60;">
            {{ in_stock_count }}
        </p>
    </div>
</div>

<div style="display: flex; gap: 15px; margin: 30px 0;">
    <a href="{% url 'product_list' %}" class="btn btn-primary">📦 Все продукты</a>
    <a href="{% url 'product_create' %}" class="btn btn-success">➕ Добавить продукт</a>
    <a href="{% url 'category_list' %}" class="btn btn-warning">📁 Категории</a>
</div>

{% if products %}
<h3>🔥 Последние добавленные продукты</h3>
<div class="product-grid">
    {% for product in products %}
    <div class="product-card">
        <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 10px;">
            <div>
                <h4 style="margin: 0; color: #333;">{{ product.name }}</h4>
                <small style="color: #666;">Артикул: {{ product.sku }}</small>
            </div>
            <div style="color: #e74c3c; font-weight: bold;">
                {{ product.price }} руб.
            </div>
        </div>
        
        <p>{{ product.description|truncatewords:15 }}</p>
        
        <div style="color: #666; font-size: 0.9em;">
            <span style="color: {% if product.status == 'in_stock' %}#27ae60{% else %}#e67e22{% endif %};">
                {{ product.get_status_display }}
            </span>
            {% if product.category %}
            <span style="margin-left: 10px;">📁 {{ product.category.name }}</span>
            {% endif %}
        </div>
        
        <div class="product-actions">
            <a href="{% url 'product_detail' product.id %}" class="btn btn-primary">Подробнее</a>
            <a href="{% url 'product_edit' product.id %}" class="btn btn-warning">Редактировать</a>
        </div>
    </div>
    {% endfor %}
</div>
{% else %}
    <div style="text-align: center; padding: 40px;">
        <h3>😔 Продукты не найдены</h3>
        <p>Пока нет добавленных продуктов. <a href="{% url 'product_create' %}">Добавьте первый продукт</a>.</p>
    </div>
{% endif %}
{% endblock %}


category_list.html:

{% extends 'product_catalog/base.html' %}

{% block title %}Категории - Каталог продуктов{% endblock %}

{% block content %}
<h2>📁 Категории продуктов</h2>

{% if categories %}
    <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 15px; margin-top: 20px;">
        {% for category in categories %}
        <div style="border: 1px solid #ddd; padding: 15px; border-radius: 8px; background: white;">
            <h3 style="margin: 0 0 10px 0;">{{ category.name }}</h3>
            {% if category.description %}
            <p style="color: #666; margin: 0 0 10px 0;">{{ category.description }}</p>
            {% endif %}
            <div style="color: #3498db; font-weight: bold;">
                Продуктов: {{ category.products.count }}
            </div>
            <div style="margin-top: 10px;">
                <a href="{% url 'product_list' %}" class="btn btn-primary">Смотреть продукты</a>
            </div>
        </div>
        {% endfor %}
    </div>
{% else %}
    <div style="text-align: center; padding: 40px;">
        <h3>📁 Категории не найдены</h3>
        <p>Пока нет добавленных категорий.</p>
    </div>
{% endif %}
{% endblock %}


Шаг 6: Обновление urls.py
Замените содержимое файла: C:\Users\VladVinnichek\Desktop\BRU\ITIWP\Labs\12\product_catalog_project\product_catalog\urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.product_list, name='product_list'),
    path('products/create/', views.product_create, name='product_create'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('products/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('categories/', views.category_list, name='category_list'),
]


Шаг 7: Применение миграций
Запустите файл Migrate.bat - он создаст и применит миграции базы данных.

Шаг 8: Создание администратора
Запустите файл SuperUser.bat - создайте учетную запись администратора для доступа к админ-панели.

Шаг 9: Запуск проекта
Запустите файл Start.bat - сервер запустится и автоматически откроется в браузере.

Шаг 10: Сделать проект публичным (Опционально)
Запустите файл Public.bat - создаст публичный URL для доступа с любого устройства.