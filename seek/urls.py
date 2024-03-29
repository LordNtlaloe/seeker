from django.urls import path
from . import views


# app_name = 'seek'
urlpatterns = [
    path('', views.home, name='home'),
    path('business/<str:business_name>/', views.business, name='business'),
    path('add-business/', views.createBusiness, name='add-business'),
    path('edit-business/<str:business_name>/', views.updateBusiness, name='edit-business'),
    path('delete-business/<str:pk>/', views.deleteBusiness, name='delete-business'),
    path('explore/', views.explore, name='explore'),
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("register/", views.registerUser, name="register"),
    path("delete-review/<str:pk>/", views.deleteReview, name="delete-review"),
    path("profile/<str:pk>/", views.userProfile, name="profile"),
    path("edit-profile/", views.editUser, name="edit-profile"),
    path("cart/", views.cart, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("update-item/", views.updateItem, name='update-item'),
    path("process-payment/", views.processOrder, name="process-payment"),
    path("products/", views.products, name="products"),
    path("business/<str:business_name>/add-product", views.addProduct, name="add-product"),
    path('business/<str:business_name>/edit-product/<str:pk>/', views.updateProduct, name='edit-product'),
    path('business/<str:business_name>/delete-product/<str:pk>/', views.deleteProduct, name='delete-product'),
    path("business/<str:business_name>/add-socials", views.addSocialLinks, name="add-socials"),
    path("business/<str:business_name>/add-opening-hours", views.addOpeningHours, name="add-opening-hours"),
]
