from django.urls import path
from . import views
from .forms import UserLoginForm

urlpatterns = [
    path('', views.index, name="index"),
    path('all_products/', views.all_products, name="products"),
    path('product/<int:prod_id>', views.singleproduct, name="product_single"),
    path('productform/', views.product_form, name="add_product"),
    path('registration/', views.UserSignupView.as_view(), name="register"),
    path('adminsignup/', views.AdminSignupView.as_view(), name="Admin register"),
    path('login/', views.Login.as_view(template_name="login.html", authentication_form=UserLoginForm), name='login'),
    path('logout/', views.logout_view, name="logout"),
    path('addbasket/<int:prod_id>', views.add_to_basket, name="add_to_basket"),
    path('basket/', views.basket, name="view_basket"),
    path('order/', views.order, name="make_order"),
    path('all_orders', views.all_orders, name="view_orders")
]
