import json

from rest_framework import response

from .serializers.Cart import CartSerializer
from .serializers.Other import UserSerializer
from ..models import *
from .serializers.Analyzes import *
from rest_framework.authtoken.models import Token

def get_cookie_cart(request):
    # Create empty cart for now for non-logged in user
    cart_products = []
    cart = {'get_cart_total': 0, 'get_cart_items_count': 0}
    cart_id = -1
    cookie_cart_data = {'cart': cart, 'cart_products': cart_products, 'cart_id': cart_id}

    try:
        cookie_cart = json.loads(request.COOKIES['cart'])
        print('CART:', cookie_cart, end='\n\n')
    except:
        cookie_cart = {}
        print('CART:', cookie_cart)
        return cookie_cart_data

    cookie_cart_data["cart_id"] = int(cookie_cart['id'])
    for p in cookie_cart['included_products']:
        # We use try block to prevent items in cart that may have been removed from causing error

        try:
            # print(f'product: {p}', end='\n\n')
            #
            # print(f'product cart id: {p["id"]}', end='\n')
            # print(f'product id: {p["product"]["id"]}', end='\n')
            # print(f'product qty: {p["qty"]}', end='\n\n')
            product_qty = p['qty']
            if product_qty > 0:  # items with negative quantity = lot of freebies

                product = Product.objects.get(id=p["product"]["id"])
                product_total = (product.price * product_qty)

                cart['get_cart_total'] += product_total
                cart['get_cart_items_count'] += product_qty

                product_base = ProductSerializer(product).data

                cart_product = {
                    'id': product.id,
                    'product': product_base,
                    'qty': product_qty,
                    'final_price': product_total,
                }
                cart_products.append(cart_product)
        except:
            pass
    # print(cookie_cart_data)
    return cookie_cart_data


def get_cart_or_create_for_anon(request):

    cookieData = get_cookie_cart(request)
    cart_id = cookieData['cart_id']
    cart = Cart.objects.filter(id=cart_id).first()
    print(cart, sep='\n\n')
    if cart is None or not cart.for_anonymous_user:
        items = cookieData['cart_products']

        cart = Cart.objects.create(
            owner=None,
            in_order=False,
            for_anonymous_user=True,
        )

        for item in items:
            product = Product.objects.get(id=item["product"]["id"])
            cartItem = CartItem.objects.create(
                product=product,
                cart=cart,
                qty=(item['qty'] if item['qty'] > 0 else -1 * item['qty']),
                # negative quantity = freebies
            )
            cartItem.save()
        print(cart, cart.id, sep=' | ')
    return cart


def create_new_anon():
    user_last_id = User.objects.all().last().id
    new_anon_user_id = user_last_id + 1
    new_anonymous_username = f'unknown{new_anon_user_id}'
    new_anonymous = User.objects.create_user(new_anonymous_username)
    token, created = Token.objects.get_or_create(user=new_anonymous)
    return new_anonymous, token.key


def get_complexes_by_type(complex_types):  # list of qs
    complexes = []
    for complex_type in complex_types:
        complex_type_obj = ComplexType.objects.get(slug=complex_type)
        qs_c = AnalyzeComplex.objects.filter(complex_type=complex_type_obj)
        complexes.extend(get_product_list_from_qs(qs_c))

    return complexes


def get_analyzes_by_search_group(search_groups):  # list of qs
    analyzes = []
    for search_group in search_groups:
        search_group_obj = SearchGroup.objects.get(slug=search_group)
        qs_a = Analyze.objects.filter(search_group=search_group_obj)
        analyzes.extend(get_product_list_from_qs(qs_a))
    return analyzes


def get_product_list_from_qs(complex_qs):  # list of model obj
    products = []
    for item in complex_qs:
        product_id = item.id
        product = Product.objects.get(pk=product_id)
        products.append(ProductSerializer(product).data)
    return products



