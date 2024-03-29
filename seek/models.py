from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    # username = models.CharField(unique=True, null=True, max_length=200)
    bio = models.TextField(max_length=200, null=True, blank=True)
    email = models.EmailField(unique=True, null=True)
    phone_number = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    profile_picture = models.ImageField(null=True, default="profile.jpeg")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.user.first_name

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.first_name

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.first_name
    
class Administrator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.first_name


class Organization(models.Model):   
    teacher = models.ManyToOneRel(Teacher, on_delete=models.CASCADE)
    student = models.ManyToOneRel(Student, on_delete=models.CASCADE)
    administrator = models.ManyToOneRel(Administrator, on_delete=models.CASCADE)


# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=200)
    category_description = models.TextField(null=True)
    category_icon = models.CharField(max_length=200, null=True)
    category_color = models.CharField(max_length=200, null=True )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category_name

class Business(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    business_name = models.CharField(max_length=200, unique=True)
    business_description = models.TextField(null=True )
    business_location = models.CharField(max_length=200, null=True)
    # business_logo = models.ImageField(null=True, default='logo.png')
    # business_cover = models.ImageField(null=True, default='background.jpg')
    # category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at', '-updated_at']

    def __str__(self):
        return self.business_name
    
class Product(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, null=True)
    product_name = models.CharField(max_length=200)
    product_description = models.TextField(null=True )
    product_price = models.DecimalField(max_digits=10, decimal_places=2, null=True )
    product_image = models.ImageField(null=True, default='product.jpeg')
    # product_category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    overall_ratings = models.IntegerField(null=True )
    hospitality = models.IntegerField(null=True )
    service = models.IntegerField(null=True )
    pricing = models.IntegerField(null=True )
    product_image = models.ImageField(null=True )
    message = models.TextField(null=True)
    business = models.ForeignKey(Business, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message[0:50]

class Socials(models.Model):
    platform_name = models.CharField(max_length=255, null=True )
    platform_link = models.CharField(max_length=255, null=True )
    business = models.ForeignKey(Business, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.business.business_name
    
class Hours(models.Model):
    monday_open = models.TimeField(auto_now_add=False, null=True)
    monday_close = models.TimeField(auto_now_add=False, null=True)
    tuesday_open = models.TimeField(auto_now_add=False, null=True)
    tuesday_close = models.TimeField(auto_now_add=False, null=True)
    wednesday_open = models.TimeField(auto_now_add=False, null=True)
    wednesday_close = models.TimeField(auto_now_add=False, null=True)
    thursday_open = models.TimeField(auto_now_add=False, null=True)
    thursday_close = models.TimeField(auto_now_add=False, null=True)
    friday_open = models.TimeField(auto_now_add=False, null=True)
    friday_close = models.TimeField(auto_now_add=False, null=True)
    saturday_open = models.TimeField(auto_now_add=False, null=True)
    saturday_close = models.TimeField(auto_now_add=False, null=True)
    sunday_open = models.TimeField(auto_now_add=False, null=True)
    sunday_close = models.TimeField(auto_now_add=False, null=True)
    business = models.ForeignKey(Business, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.business.business_name

class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    
    @property
    def shipping(self):
        shipping = True
        return shipping

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.product_name

    @property
    def get_total(self):
        total = self.product.product_price * self.quantity
        return total
    
class ShippingAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.address