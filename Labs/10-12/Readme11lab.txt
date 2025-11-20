Полная инструкция по настройке Django проекта "Product Catalog (продолжение 10 лабораторной)"

Для повторного запуска пусле перезагрузки ПК нужно запустить только Start.bat, и если нужен публичный URL: Public.bat!!!

Шаг 1: Обновление models.py
Замените полное содержимое файла:
C:\Users\VladVinnichek\Desktop\BRU\ITIWP\Labs\11\product_catalog_project\product_catalog\models.py

from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")
    description = models.TextField(blank=True, verbose_name="Описание категории")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']

class Product(models.Model):
    STATUS_CHOICES = [
        ('in_stock', 'В наличии'),
        ('out_of_stock', 'Нет в наличии'),
        ('discontinued', 'Снят с производства'),
    ]
    
    name = models.CharField(max_length=200, verbose_name="Название продукта")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Цена",
        validators=[MinValueValidator(0)]
    )
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        verbose_name="Категория",
        related_name='products',
        null=True,
        blank=True
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='in_stock',
        verbose_name="Статус"
    )
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=0,
        verbose_name="Рейтинг",
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    sku = models.CharField(
        max_length=50, 
        unique=True, 
        verbose_name="Артикул (SKU)"
    )
    is_active = models.BooleanField(default=True, verbose_name="Активный")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    def __str__(self):
        return f"{self.name} ({self.sku})"
    
    def get_created_at_local(self):
        return timezone.localtime(self.created_at)
    
    def get_updated_at_local(self):
        return timezone.localtime(self.updated_at)
    
    @property
    def availability_status(self):
        return dict(self.STATUS_CHOICES).get(self.status, 'Неизвестно')
    
    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'is_active']),
            models.Index(fields=['category', 'created_at']),
        ]

class ProductAttribute(models.Model):
    ATTRIBUTE_TYPES = [
        ('color', 'Цвет'),
        ('size', 'Размер'),
        ('material', 'Материал'),
        ('weight', 'Вес'),
        ('dimensions', 'Габариты'),
        ('warranty', 'Гарантия'),
        ('brand', 'Бренд'),
        ('country', 'Страна производства'),
        ('other', 'Другое'),
    ]
    
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Продукт",
        related_name='attributes'
    )
    attribute_type = models.CharField(
        max_length=20,
        choices=ATTRIBUTE_TYPES,
        verbose_name="Тип атрибута"
    )
    value = models.CharField(max_length=200, verbose_name="Значение атрибута")
    display_order = models.PositiveIntegerField(
        default=0,
        verbose_name="Порядок отображения"
    )
    
    def __str__(self):
        attribute_name = dict(self.ATTRIBUTE_TYPES).get(self.attribute_type, self.attribute_type)
        return f"{self.product.name} - {attribute_name}: {self.value}"
    
    class Meta:
        verbose_name = "Атрибут продукта"
        verbose_name_plural = "Атрибуты продуктов"
        ordering = ['product', 'display_order', 'attribute_type']
        unique_together = ['product', 'attribute_type']


Шаг 2: Обновление admin.py
Замените полное содержимое файла:
C:\Users\VladVinnichek\Desktop\BRU\ITIWP\Labs\11\product_catalog_project\product_catalog\admin.py

from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html
from .models import Category, Product, ProductAttribute

class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 1
    fields = ['attribute_type', 'value', 'display_order']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'product_count', 'formatted_created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['formatted_created_at']
    
    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Количество продуктов'
    
    def formatted_created_at(self, obj):
        return timezone.localtime(obj.created_at).strftime('%d.%m.%Y %H:%M')
    formatted_created_at.short_description = 'Дата создания'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name', 
        'sku', 
        'category', 
        'price', 
        'status_badge', 
        'rating', 
        'is_active',
        'formatted_created_at'
    ]
    list_filter = ['status', 'is_active', 'category', 'created_at']
    search_fields = ['name', 'description', 'sku']
    readonly_fields = ['formatted_created_at', 'formatted_updated_at']
    list_editable = ['price', 'rating', 'is_active']
    inlines = [ProductAttributeInline]
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'description', 'sku', 'category', 'price')
        }),
        ('Дополнительная информация', {
            'fields': ('status', 'rating', 'is_active')
        }),
        ('Системная информация', {
            'fields': ('formatted_created_at', 'formatted_updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def status_badge(self, obj):
        status_colors = {
            'in_stock': 'green',
            'out_of_stock': 'orange',
            'discontinued': 'red'
        }
        color = status_colors.get(obj.status, 'gray')
        status_text = dict(Product.STATUS_CHOICES).get(obj.status, 'Неизвестно')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 8px; border-radius: 12px; font-size: 12px;">{}</span>',
            color, status_text
        )
    status_badge.short_description = 'Статус'
    
    def formatted_created_at(self, obj):
        return timezone.localtime(obj.created_at).strftime('%d.%m.%Y %H:%M')
    formatted_created_at.short_description = 'Дата создания'
    
    def formatted_updated_at(self, obj):
        return timezone.localtime(obj.updated_at).strftime('%d.%m.%Y %H:%M')
    formatted_updated_at.short_description = 'Дата обновления'

@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ['product', 'get_attribute_type_display', 'value', 'display_order']
    list_filter = ['attribute_type', 'product__category']
    search_fields = ['value', 'product__name']
    list_editable = ['value', 'display_order']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('product')


Шаг 3: Обновление views.py
Замените полное содержимое файла:
C:\Users\VladVinnichek\Desktop\BRU\ITIWP\Labs\11\product_catalog_project\product_catalog\views.py

from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from .models import Product, ProductAttribute

def index(request):
    products = Product.objects.filter(is_active=True).select_related('category').prefetch_related('attributes')
    current_time = timezone.localtime(timezone.now()).strftime('%d.%m.%Y %H:%M')
    
    response = f"""
    <html>
    <head>
        <title>Каталог продуктов</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .product {{ border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; }}
            .product-header {{ display: flex; justify-content: space-between; align-items: center; }}
            .product-name {{ font-size: 1.2em; font-weight: bold; color: #333; }}
            .product-price {{ font-size: 1.3em; color: #e74c3c; font-weight: bold; }}
            .product-sku {{ color: #666; font-size: 0.9em; }}
            .product-category {{ background: #f8f9fa; padding: 2px 8px; border-radius: 3px; font-size: 0.9em; }}
            .attributes {{ margin-top: 10px; }}
            .attribute {{ display: inline-block; background: #e8f4fd; padding: 4px 8px; margin: 2px; border-radius: 3px; font-size: 0.9em; }}
            .status-in_stock {{ color: #27ae60; }}
            .status-out_of_stock {{ color: #e67e22; }}
            .status-discontinued {{ color: #95a5a6; }}
        </style>
    </head>
    <body>
        <h1>🛍️ Добро пожаловать в каталог продуктов</h1>
        <p><strong>Время:</strong> {current_time}</p>
        <hr>
        <h2>📦 Список продуктов:</h2>
    """
    
    if products:
        for product in products:
            created_at = timezone.localtime(product.created_at).strftime('%d.%m.%Y %H:%M')
            
            # Формируем HTML для атрибутов
            attributes_html = ""
            if product.attributes.exists():
                attributes_html = "<div class='attributes'>"
                for attr in product.attributes.all():
                    attributes_html += f"<span class='attribute'><strong>{attr.get_attribute_type_display()}:</strong> {attr.value}</span>"
                attributes_html += "</div>"
            
            # Статус продукта
            status_class = f"status-{product.status}"
            status_text = product.get_status_display()
            
            response += f"""
            <div class="product">
                <div class="product-header">
                    <div>
                        <div class="product-name">{product.name}</div>
                        <div class="product-sku">Артикул: {product.sku}</div>
                    </div>
                    <div class="product-price">{product.price} руб.</div>
                </div>
                
                <p>{product.description}</p>
                
                {attributes_html}
                
                <div style="margin-top: 10px;">
                    <span class="{status_class}">📊 Статус: {status_text}</span>
                    <span style="margin-left: 15px;">⭐ Рейтинг: {product.rating}/5</span>
                    {f'<span style="margin-left: 15px;" class="product-category">📁 {product.category.name}</span>' if product.category else ''}
                    <span style="margin-left: 15px; color: #666; font-size: 0.9em;">📅 Добавлен: {created_at}</span>
                </div>
            </div>
            """
    else:
        response += "<p>😔 Продукты пока не добавлены</p>"
    
    response += """
        <hr>
        <p style="color: #666; font-size: 0.9em;">
            Всего продуктов: """ + str(products.count()) + """
        </p>
    </body>
    </html>
    """
    
    return HttpResponse(response)

def product_detail(request, product_id):
    try:
        product = Product.objects.filter(is_active=True).select_related('category').prefetch_related('attributes').get(id=product_id)
        created_at = timezone.localtime(product.created_at).strftime('%d.%m.%Y %H:%M')
        
        # Формируем детальную информацию об атрибутах
        attributes_html = ""
        if product.attributes.exists():
            attributes_html = "<h3>📋 Характеристики:</h3><ul>"
            for attr in product.attributes.all():
                attributes_html += f"<li><strong>{attr.get_attribute_type_display()}:</strong> {attr.value}</li>"
            attributes_html += "</ul>"
        
        response = f"""
        <html>
        <head>
            <title>{product.name}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .detail-header {{ display: flex; justify-content: space-between; align-items: start; }}
                .product-price {{ font-size: 1.5em; color: #e74c3c; font-weight: bold; }}
                .back-link {{ margin-bottom: 20px; }}
            </style>
        </head>
        <body>
            <div class="back-link">
                <a href="/">← Назад к каталогу</a>
            </div>
            
            <div class="detail-header">
                <div>
                    <h1>{product.name}</h1>
                    <p><strong>Артикул:</strong> {product.sku}</p>
                </div>
                <div class="product-price">{product.price} руб.</div>
            </div>
            
            <p><strong>Описание:</strong> {product.description}</p>
            
            {attributes_html}
            
            <div style="margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 5px;">
                <p><strong>📊 Статус:</strong> {product.get_status_display()}</p>
                <p><strong>⭐ Рейтинг:</strong> {product.rating}/5</p>
                {f'<p><strong>📁 Категория:</strong> {product.category.name}</p>' if product.category else ''}
                <p><strong>📅 Дата добавления:</strong> {created_at}</p>
            </div>
        </body>
        </html>
        """
        return HttpResponse(response)
    except Product.DoesNotExist:
        return HttpResponse("<h1>❌ Продукт не найден</h1><p>Запрошенный продукт не существует или был удален.</p>", status=404)


Шаг 4: Применение миграций
Запустите файл Migrate.bat - он создаст и применит миграции базы данных.

Шаг 5: Создание администратора
Запустите файл SuperUser.bat - создайте учетную запись администратора для доступа к админ-панели.

Шаг 6: Запуск проекта
Запустите файл Start.bat - сервер запустится и автоматически откроется в браузере.

Шаг 7: Сделать проект публичным (Опционально)
Запустите файл Public.bat - сервер запустится и автоматически откроется в браузере.