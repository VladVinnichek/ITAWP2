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