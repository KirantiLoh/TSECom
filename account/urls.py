from django.urls import path
from . import views

urlpatterns = [
    path('cart', views.cart_view, name='Cart'),
    path('profile', views.profile_view, name = 'Profile'),
    path('profile/<int:id>', views.public_profile_view, name = 'Public Profile'),
    path('register', views.register_view, name = 'register'),
    path('add_to_cart/<int:id>', views.add_to_cart, name = "Add To Cart"),
    path('checkout', views.checkout, name="Checkout"),
    path('delete_item/<int:id>', views.delete_item_from_cart, name="Delete Item"),
    path('success', views.checkout_success_view, name="Checkout Success"),
    path('fail', views.checkout_fail_view, name="Checkout Fail"),
    path('edit_profile', views.edit_profile_view, name="Edit Profile"),
]