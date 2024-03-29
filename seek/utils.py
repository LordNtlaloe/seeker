import json
import datetime
from . models import * 

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    print('Cart: ', cart)
    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0}
    cartItems = order['get_cart_items']

    for i in cart:
        try:
            cartItems += cart[i]['quantity']
            product = Product.objects.get(id=i)
            total = (product.product_price * cart[i]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            item = {
                'product' : {
                    'id' : product.id,
                    'product_name' : product.product_name,
                    'product_price' : product.product_price,
                    'product_image' : product.product_image
                },
                'quantity' : cart[i]['quantity'],
                'get_total' : total
            }
            items.append(item)
            order.shipping = True
        except:
            pass
    return {'items' : items, 'order' : order, 'cartItems' : cartItems}

def cartData(request):
    if request.user.is_authenticated:
        customer = request.user
        print(customer)
        order, created_at = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        print(items)
    else:
        cookieData = cookieCart(request)
        cartItems  = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
        
    print(items)
    return {'items' : items, 'order' : order, 'cartItems' : cartItems}


def guestOrder(request, data):
    print('User Is Not Logged In')
    transaction_id = datetime.datetime.now().timestamp()

    print('COOKIES: ', request.COOKIES)
    first_name = data['form']['firstName']
    last_name = data['form']['lastName']
    email = data['form']['email']
    phone_number = data['form']['phoneNumber']

    cookieData = cookieCart(request)
    items = cookieData['items']

    customer, created_at = Customer.objects.get_or_create(
        email = email,
    )
    customer.first_name = first_name
    customer.last_name = last_name
    customer.phone_number = phone_number
    customer.save()

    order = Order.objects.create(
        customer = customer,
        completed = False
    )

    for item in items:
        product = Product.objects.get(id = item['product']['id'])
        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
        )
    return customer, order