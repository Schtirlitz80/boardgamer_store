from django.contrib import admin
from shop.models import Product


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}



# name = models.CharField(max_length=200, db_index=True)
# slug = models.SlugField(max_length=200, db_index=True)
# image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
# short_description = models.TextField(blank=True)
# description = models.TextField(blank=True)
# price = models.DecimalField(max_digits=10, decimal_places=2)
# available = models.BooleanField(default=True)
# created = models.DateTimeField(auto_now_add=True)
# updated = models.DateTimeField(auto_now=True)