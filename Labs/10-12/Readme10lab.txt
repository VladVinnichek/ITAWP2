Полная инструкция по настройке Django проекта "Product Catalog"

Для повторного запуска пусле перезагрузки ПК нужно запустить только Start.bat, и если нужен публичный URL: Public.bat!!!

Шаг 1: Установка проекта
Запустите файл Install.bat - он создаст виртуальное окружение, установит Django и создаст проект с приложением.

Шаг 2: Настройка settings.py
Откройте файл: C:\Users\VladVinnichek\Desktop\BRU\ITIWP\Labs\10\product_catalog_project\product_catalog_project\settings.py

Найдите строку ALLOWED_HOSTS = ['(или *)'] и замените её на::
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '.trycloudflare.com']

После блока ALLOWED_HOSTS добавьте:
CSRF_TRUSTED_ORIGINS = [
    'https://*.trycloudflare.com',
    'http://127.0.0.1:8000',
    'http://localhost:8000',
]

# CORS settings for development
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# Cookie settings for development
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SAMESITE = 'Lax'

Добавьте в INSTALLED_APPS:
'product_catalog',

Вот так:
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'product_catalog',
]


Замените раздел Internationalization на:

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Minsk'
USE_I18N = True
USE_L10N = True
USE_TZ = True

DATE_FORMAT = 'd.m.Y'
TIME_FORMAT = 'H:i'
DATETIME_FORMAT = 'd.m.Y H:i'
SHORT_DATE_FORMAT = 'd.m.Y'
SHORT_DATETIME_FORMAT = 'd.m.Y H:i'

USE_THOUSAND_SEPARATOR = True
THOUSAND_SEPARATOR = ' '
NUMBER_GROUPING = 3
DECIMAL_SEPARATOR = ','

Шаг 3: Замена кода в Python файлах

models.py
Замените полное содержимое файла:
C:\Users\VladVinnichek\Desktop\BRU\ITIWP\Labs\10\product_catalog_project\product_catalog\models.py

from django.db import models
from django.utils import timezone

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название продукта")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    def __str__(self):
        return self.name
    
    def get_created_at_local(self):
        return timezone.localtime(self.created_at)
    
    def get_updated_at_local(self):
        return timezone.localtime(self.updated_at)
    
    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ['-created_at']


admin.py
Замените полное содержимое файла:
C:\Users\VladVinnichek\Desktop\BRU\ITIWP\Labs\10\product_catalog_project\product_catalog\admin.py

from django.contrib import admin
from django.utils import timezone
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'formatted_created_at', 'formatted_updated_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    
    def formatted_created_at(self, obj):
        return timezone.localtime(obj.created_at).strftime('%d.%m.%Y %H:%M')
    formatted_created_at.short_description = 'Дата создания'
    
    def formatted_updated_at(self, obj):
        return timezone.localtime(obj.updated_at).strftime('%d.%m.%Y %H:%M')
    formatted_updated_at.short_description = 'Дата изменения'


views.py
Замените полное содержимое файла:
C:\Users\VladVinnichek\Desktop\BRU\ITIWP\Labs\10\product_catalog_project\product_catalog\views.py

from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from .models import Product

def index(request):
    products = Product.objects.all()
    current_time = timezone.localtime(timezone.now()).strftime('%d.%m.%Y %H:%M')
    
    response = f"""
    <h1>Добро пожаловать в каталог продуктов</h1>
    <p><strong>Время:</strong> {current_time}</p>
    <hr>
    <h2>Список продуктов:</h2>
    """
    
    if products:
        for product in products:
            created_at = timezone.localtime(product.created_at).strftime('%d.%m.%Y %H:%M')
            response += f"""
            <div style="border: 1px solid #ccc; padding: 10px; margin: 10px 0;">
                <h3>{product.name}</h3>
                <p><strong>Описание:</strong> {product.description}</p>
                <p><strong>Цена:</strong> {product.price} руб.</p>
                <p><strong>Добавлен:</strong> {created_at}</p>
            </div>
            """
    else:
        response += "<p>Продукты пока не добавлены</p>"
    
    return HttpResponse(response)

def product_detail(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        created_at = timezone.localtime(product.created_at).strftime('%d.%m.%Y %H:%M')
        response = f"""
        <h1>{product.name}</h1>
        <p><strong>Описание:</strong> {product.description}</p>
        <p><strong>Цена:</strong> {product.price} руб.</p>
        <p><strong>Создан:</strong> {created_at}</p>
        """
        return HttpResponse(response)
    except Product.DoesNotExist:
        return HttpResponse("Продукт не найден", status=404)


urls.py (приложения)
Создайте файл: C:\Users\VladVinnichek\Desktop\BRU\ITIWP\Labs\10\product_catalog_project\product_catalog\urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
]


urls.py (проекта)
Замените полное содержимое файла:
C:\Users\VladVinnichek\Desktop\BRU\ITIWP\Labs\10\product_catalog_project\product_catalog_project\urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('product_catalog.urls')),
]


Шаг 4: Применение миграций
Запустите файл Migrate.bat - он создаст и применит миграции базы данных.

Шаг 5: Создание администратора
Запустите файл SuperUser.bat - создайте учетную запись администратора для доступа к админ-панели.

Шаг 6: Запуск проекта
Запустите файл Start.bat - сервер запустится и автоматически откроется в браузере.

Шаг 7: Сделать проект публичным (Опционально)
Запустите файл Public.bat - сервер запустится и автоматически откроется в браузере.