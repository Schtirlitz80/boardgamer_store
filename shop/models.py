from django.db import models
from django.urls import reverse

import json
from django.utils.text import slugify
from uuid import uuid4
from pytils.translit import slugify


def unique_slugify(instance, slug):
    """
    Генератор уникальных SLUG для моделей, в случае существования такого SLUG.
    """
    model = instance.__class__
    unique_slug = slugify(slug)
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = f'{unique_slug}-{uuid4().hex[:8]}'
    return unique_slug


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    short_description = models.TextField(blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.IntegerField(default=0)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Сохранение полей модели при их отсутствии заполнения
        """
        if not self.slug:
            self.slug = unique_slugify(self, self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])


def fill_db():
    with open('products_scraped/products.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

        for item in data[:300]:
            product = Product()

            num = item["num"]
            product.name = item["product_name"]
            price_str = item["price"]
            price_lst = price_str.split('.')
            product.price = int(price_lst[0])+int(price_lst[1][:2])/100
            product.short_description = item["short_description"]
            product.description = item["full_description"]
            product.available = True
            image_filename = item["image_filename"]
            product.image = 'products/2023/03/05/' + image_filename

            print(product)
            print(item)
            product.save()


if __name__ == '__main__':
    fill_db()

