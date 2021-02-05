from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('registration/', views.register, name="register"),
    path('all_products/', views.all_products, name="products"),
    path('product/<int:prod_id>', views.singleproduct, name="product_single"),
    path('productform/', views.product_form, name="add_product")
]
