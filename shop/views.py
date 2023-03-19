from django.shortcuts import render, get_object_or_404
from .forms import ProductForm
from .models import Product, ProductImage


# Create your views here.
def home(request):
    products = Product.objects.filter(available=True)
    product_images = ProductImage.objects.filter(is_active=True, is_main=True, product__available=True)
    # Категорий продуктов у нас пока нет

    # return render(request, 'shop/product/home.html', {'products': products})
    return render(request, 'shop/product/home.html', locals())


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)

    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()
    print("request.session.session_key: ", request.session.session_key)

    return render(request, 'shop/product/detail.html', locals())
