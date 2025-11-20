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