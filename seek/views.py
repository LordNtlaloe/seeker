from django.shortcuts import render, redirect
from .models import Category, Business, Product, Hours, Socials, Customer, Review, User, Order, OrderItem, ShippingAddress
from django.db.models import Q
from .forms import BusinessForm, UserForm, UserRegisrationForm, ProductForm, SocialsForm, HoursForm
from django.contrib import messages
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
import json
import datetime
from .utils import cookieCart, cartData, guestOrder
from urllib.parse import urlparse


# Create your views here.

#everythin Business Model Related
def home(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = ['items']
        
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    businesses = Business.objects.filter(Q(category__category_name__icontains=q) | Q(business_name__icontains=q) | Q(business_description__icontains=q))
    products = Product.objects.filter(Q(product_name__icontains=q) | Q(product_description__icontains=q))
    category = Category.objects.all().order_by('-created_at')[0:4]
    # print(cartItems)
    context = {
        'products' : products,
        'businesses' : businesses,
        'category' : category,
        'items' : items,
        'cartItems' : cartItems
    }
    # print(cartItems)
    return render(request, 'seek/index.html', context)

def business(request, business_name):
    data = cartData(request)
    cartItems = data['cartItems']
    items = ['items']

    business = Business.objects.get(business_name = business_name)
    products = business.product_set.all().order_by('-created_at')
    reviews =  business.review_set.all().order_by('-created_at')
    socials = business.socials_set.all().order_by('-created_at')
    hours = business.hours_set.all()
    # print(socials.facebook)
    for social in socials:
        social_link = social.platform_link
        print(social_link)
    
    if request.method == 'POST':
        review = Review.objects.create(
            user = request.user,
            business = business,
            message = request.POST.get('message')
        )
        return redirect('business', business_name=business.business_name)
    
    # if request.method == 'POST':
    #     product = Product.objects.create(
    #         business = business,
    #         product_name = request.POST.get('product_name'),
    #         product_description = request.POST.get('product_description'),
    #         product_price = request.POST.get('product_price')
    #     )
    #     return redirect('business', business_name=business.business_name)

    context = {
        'business' : business,
        'products' : products,
        'reviews' : reviews,
        'socials' : socials,
        'items' : items,
        'cartItems' : cartItems,
        'hours' : hours
    }
    return render(request, 'seek/business/business.html', context)

@login_required(login_url='login')
def createBusiness(request):
    data = cartData(request)
    cartItems = data['cartItems']
    items = ['items']
    form = BusinessForm()
    if request.method == 'POST':
        form = BusinessForm(request.POST, request.FILES)
        if form.is_valid():
            business = form.save(commit=False)
            business.user = request.user
            business.save()
            return redirect('/')
    context = { 
        'form' : form,
        'items' : items,
        'cartItems' : cartItems
    }
    return render(request, 'seek/business/form.html', context)

@login_required(login_url='login/')
def updateBusiness(request, business_name):
    data = cartData(request)
    cartItems = data['cartItems']
    items = ['items']

    business = Business.objects.get(business_name = business_name)
    form = BusinessForm(instance=business)

    if request.user != business.user:
        return HttpResponse('This Is A Restricted Area')

    if request.method == 'POST':
        form = BusinessForm(request.POST, request.FILES,  instance=business)
        if form.is_valid():
            form.save() 
            return redirect('/')
    context = {
        'form' : form,
        'cartItems' : cartItems,
        'items' : items
    }
    return render(request, 'seek/business/form.html', context)

@login_required(login_url='login/')
def deleteBusiness(request, pk):
    data = cartData(request)
    cartItems = data['cartItems']
    items = ['items']

    business = Business.objects.get(id=pk)
    if request.user != business.user:
        return HttpResponse('This Is A Restricted Area')
    if request.method == 'POST':
        business.delete()
        return redirect('/')
    return render(request, 'seek/delete.html', {'obj' : business, 'items' : items, 'cartitems' : cartItems})


# @login_required(login_url='login/')
def products(request):
    data = cartData(request)
    cartItems = data['cartItems']
    items = ['items']

    q = request.GET.get('q') if request.GET.get('q') != None else ''
    products = Product.objects.filter(Q(business__business_name__icontains=q) | Q(product_name__icontains=q) | Q(product_description__icontains=q))
    business = Business.objects.all()
    search_count = products.count()
    context = {
        'products' : products,
        'business' : business,
        'search_count' : search_count,
        'items' : items,
        'cartItems' : cartItems
    }
    return render(request, 'seek/product/products.html', context)

@login_required(login_url='login/')
def addProduct(request, business_name):
    data = cartData(request)
    cartItems = data['cartItems']
    items = ['items']

    business = Business.objects.get(business_name = business_name)
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.business = business
            product.save()
            return redirect('/')
    context = { 
        'form' : form,
        'cartItems' : cartItems,
        'items' : items
    }
    return render(request, 'seek/product/form.html', context)


@login_required(login_url='login/')
def updateProduct(request, business_name, pk):
    data = cartData(request)
    cartItems = data['cartItems']
    items = ['items']

    business = Business.objects.get(business_name = business_name)
    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product)

    if request.user != business.user:
        return HttpResponse('This Is A Restricted Area')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES,  instance=product)
        if form.is_valid():
            form.save()
            product.save()
            return redirect('/')
    context = {
        'form' : form,
        'items' : items,
        'cartItems' : cartItems
    }
    return render(request, 'seek/product/form.html', context)

@login_required(login_url='login/')
def deleteProduct(request, business_name, pk):
    data = cartData(request)
    cartItems = data['cartItems']
    items = ['items']

    business = Business.objects.get(business_name = business_name)
    product = Product.objects.get(id=pk)
    if request.user != business.user:
        return HttpResponse('This Is A Restricted Area')
    if request.method == 'POST':
        product.delete()
        return redirect('/')
    return render(request, 'seek/delete.html', {'obj' : product, 'cartItems' : cartItems, 'items' : items})


#Other Pages
def explore(request):
    data = cartData(request)
    cartItems = data['cartItems']
    items = ['items']

    q = request.GET.get('q') if request.GET.get('q') != None else ''
    businesses = Business.objects.filter(Q(category__category_name__icontains=q) | Q(business_name__icontains=q) | Q(business_description__icontains=q))
    category = Category.objects.all()
    search_count = businesses.count()
    context = {
        'businesses' : businesses,
        'category' : category,
        'search_count' : search_count,
        'items' : items,
        'cartItems' : cartItems
    }
    return render(request, 'seek/explore.html', context)

def loginPage(request):

    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User Not Found')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('/', messages.success(request, 'User Login Successful'))
        else:
            messages.success(request, 'Invalid Username Or Password')
        
    return render(request, 'seek/login.html')

def logoutUser(request):
    logout(request)
    return redirect('/')


def registerUser(request):
    data = cartData(request)
    cartItems = data['cartItems']
    items = ['items']

    form = UserRegisrationForm()

    if request.method == 'POST':
        form = UserRegisrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Could Not Complete Registration. An Error Occured')
    return render(request, 'seek/register.html', {'form' : form, 'cartItems' : cartItems, 'items' : items})

@login_required(login_url='login')
def userProfile(request, pk):
    data = cartData(request)
    cartItems = data['cartItems']
    items = ['items']

    user = User.objects.get(id=pk)
    businesses = user.business_set.all()
    context = {
        'user' : user,
        'businesses' : businesses,
        'cartItems' : cartItems,
        'items' : items
        }
    return render(request, 'seek/user/profile.html', context)

@login_required(login_url='login')
def editUser(request):
    data = cartData(request)
    cartItems = data['cartItems']
    items = ['items']

    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid:
            form.save()
            return redirect('profile', pk=user.id)
    context = {
        'form' : form,
        'cartItems' : cartItems,
        'items' : items
    }
    return render(request, 'seek/user/edit-profile.html', context)

@login_required(login_url='login')
def deleteReview(request, pk):
    data = cartData(request)
    cartItems = data['cartItems']
    items = ['items']

    review = Review.objects.get(id=pk)
    if request.user != review.user:
        return HttpResponse('This Is A Restricted Area')
    if request.method == 'POST':
        review.delete()
        return redirect('/')
    return render(request, 'seek/delete.html', {'obj' : review, 'items' : items, 'cartItems' : cartItems})

def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    print(items)
    context = {'items' : items, 'order' : order, 'cartItems' : cartItems}
    return render(request, 'seek/orders/cart.html', context)

def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    context = {'items' : items, 'order' : order, 'cartItems' : cartItems}
    return render(request, 'seek/orders/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print(productId)
    print(action)

    customer = request.user
    product = Product.objects.get(id=productId)
    order, created_at = Order.objects.get_or_create(customer=customer, completed=False)
    orderItem, created_at = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item Was Added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user
        order, created_at = Order.objects.get_or_create(customer=customer, completed=False)
    else:
        customer, order = guestOrder(request, data)
    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    if total == order.get_cart_total:
        order.completed = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer = customer,
            order = order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            village = data['shipping']['village'],
            zipcode = data['shipping']['zipcode'],
        )
    return JsonResponse('Payment Submitted...', safe=False)

@login_required(login_url='login')
def addSocialLinks(request, business_name):
    data = cartData(request)
    cartItems = data['cartItems']
    items = ['items']

    business = Business.objects.get(business_name = business_name)
    form = SocialsForm()
    if request.method == 'POST':
        form = SocialsForm(request.POST)
        if form.is_valid():
            socials = form.save(commit=False)
            socials.business = business
            socials.save()
            return redirect('/')
    context = { 
        'form' : form,
        'cartItems' : cartItems,
        'items' : items
    }
    return render(request, 'seek/socials/form.html', context)

@login_required(login_url='login')
def addOpeningHours(request, business_name):
    data = cartData(request)
    cartItems = data['cartItems']
    items = ['items']

    business = Business.objects.get(business_name = business_name)
    form = HoursForm()
    if request.method == 'POST':
        form = HoursForm(request.POST)
        if form.is_valid():
            hours = form.save(commit=False)
            hours.business = business
            hours.save()
            return redirect('/')
    context = { 
        'form' : form,
        'cartItems' : cartItems,
        'items' : items
    }
    return render(request, 'seek/hours/form.html', context)