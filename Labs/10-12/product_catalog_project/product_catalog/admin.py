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