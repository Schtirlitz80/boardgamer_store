from django.shortcuts import render, get_object_or_404
from .forms import ProductForm
from .models import Product


# Create your views here.
def home(request):
    products = Product.objects.filter(available=True)
    # Категорий продуктов у нас пока нет

    return render(request, 'shop/product/home.html',
                  {'products': products})


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    return render(request, 'shop/product/detail.html', {'product': product})
