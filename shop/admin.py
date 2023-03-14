from django.contrib import admin
from shop.models import Product, ProductImage


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'discount', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated', 'discount']
    list_editable = ['price', 'available', 'discount']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image', 'is_main', 'is_active', 'created', 'updated']
