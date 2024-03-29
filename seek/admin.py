from django.contrib import admin
from .models import User, Category, Business, Product, Socials, Hours, Review, Order, OrderItem, ShippingAddress, Customer

# Register your models here.
admin.site.register(Category)
admin.site.register(Business)
admin.site.register(Product)
admin.site.register(Socials)
admin.site.register(Hours)
admin.site.register(Review)
admin.site.register(User)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Customer)

