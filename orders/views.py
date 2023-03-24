from django.shortcuts import render
from django.http import JsonResponse
from .models import ProductInBasket

# Create your views here.
def basket_adding(request):
    return_dict = dict()
    session_key = request.session.session_key
    data = request.POST
    print(data)
    product_id = data.get("product_id")
    nmb = data.get("nmb")

    new_product, created = ProductInBasket.objects.get_or_create(session_key=session_key, product_id=product_id, defaults={"mnb": nmb})
    if not created:
        new_product.nmb += int(nmb)
        new_product.save(force_update=True)

    products_total_nmb = ProductInBasket.objects.filter(session_key=session_key, is_active=True).count()
    return_dict["products_total_nmb"] = products_total_nmb

    return JsonResponse(return_dict)
