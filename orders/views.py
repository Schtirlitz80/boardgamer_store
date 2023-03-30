from django.http import JsonResponse
from django.shortcuts import render
from .models import *
from .forms import CheckoutContactForm
from django.contrib.auth.models import User


# Create your views here.
def basket_adding(request):  # request.POST получаем из $.ajax({})
    return_dict = dict()
    session_key = request.session.session_key
    data = request.POST
    product_id = data.get("product_id")
    nmb = data.get("nmb")
    is_delete = data.get("is_delete")

    if is_delete == 'true':
        ProductInBasket.objects.filter(product_id=product_id).update(is_active=False)
    else:
        new_product, created = ProductInBasket.objects.get_or_create(session_key=session_key,
                                                                     product_id=product_id,
                                                                     is_active=True,
                                                                     defaults={"nmb": nmb})
        if not created:
            new_product.nmb += int(nmb)
            new_product.save(force_update=True)

    # common code for both cases
    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True)
    products_total_nmb = products_in_basket.count()
    return_dict["products_total_nmb"] = products_total_nmb

    return_dict["products"] = list()

    for item in products_in_basket:
        product_dict = dict()
        product_dict["id"] = item.id
        product_dict["product_id"] = item.product_id
        product_dict["name"] = item.product.name
        product_dict["price_per_item"] = item.price_per_item
        product_dict["nmb"] = item.nmb

        return_dict["products"].append(product_dict)

    return JsonResponse(return_dict)


def checkout(request):
    session_key = request.session.session_key
    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True, order__isnull=True)
    form = CheckoutContactForm(request.POST or None)
    if request.POST:
        print(request.POST)
        if form.is_valid():
            print('form is valid')
            data = request.POST
            name = data.get('name', 'name_is_unknown')  # второе значение по умолчанию
            phone = data["phone"]
            user, created = User.objects.get_or_create(username=phone, defaults={'first_name': name})

            try:
                print(f"Arguments for 'order' object creation: user={user}, customer_name={name}, customer_phone={phone}, status_id=1")
                order = Order.objects.create(user=user, customer_name=name, customer_phone=phone, status_id=1)
                print("Order object is created successfully")
            except Exception as e:
                print("Can't create an order: ", e)

            for name, value in data.items():
                if name.startswith('product_in_basket_'):
                    product_in_basket_id = name.split('_')[-1]
                    print('product_in_basket_id: ', product_in_basket_id)
                    product_in_basket = ProductInBasket.objects.get(id=product_in_basket_id)
                    product_in_basket.nmb = value
                    product_in_basket.order = order
                    product_in_basket.save(force_update=True)

                    ProductInOrder.objects.create(product=product_in_basket.product,
                                                  nmb=product_in_basket.nmb,
                                                  price_per_item=product_in_basket.price_per_item,
                                                  total_price=product_in_basket.total_price,
                                                  order=order)

        else:
            print('NOT valid form!')
    return render(request, 'shop/orders/checkout.html', locals())
