from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name = 'Home'),
    path('get_started', views.get_started_view, name = 'Get Started'),
    path('search', views.search_result_view, name='Search'),
    path('product/<int:id>', views.product_view, name='Product'),
    path('products', views.all_product_view, name='All Products'),
    path('add_product', views.add_product_view, name='Add Product'),
    path('bought_items', views.bought_item_view, name='Bought Items'),
    path('add_review/<int:id>', views.add_review_view, name='Add Review'),
    path('restock/<int:id>', views.restock_view, name='Restock'),
    path('edit_product/<int:id>', views.edit_product_view, name='Edit Product'),
    path('delete_product/<int:id>', views.delete_product, name='Delete Product'),
    path('send_message', views.send_message, name='Send Message'),
]