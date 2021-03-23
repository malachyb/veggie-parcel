from django.urls import path
from . import views
from .forms import UserLoginForm

urlpatterns = [
    path('', views.index, name="index"),
    path('all_products/', views.all_products, name="products"),
    path('product/<int:prod_id>', views.singleproduct, name="product_single"),
    path('productform/', views.product_form, name="add_product"),
    path('usersignup/', views.UserSignupView.as_view(), name="register"),
    path('admin_signup/', views.AdminSignupView.as_view(), name="Admin register"),
    path('login/', views.Login.as_view(template_name="login.html", authentication_form=UserLoginForm), name='login'),
    path('logout/', views.logout_view, name="logout"),
    path('addbasket/<int:prod_id>', views.add_to_basket, name="add_to_basket"),
    path('basket/', views.basket, name="view_basket"),
    path('order/', views.order, name="make_order"),
    path('admin_all_orders/', views.all_orders, name="view_orders"),
    path('admin_view_order/<int:order_id>', views.view_order, name="view_order"),
    path('complete_order/<int:order_id>', views.complete_order, name="complete_order"),
    path('remove_basket/<int:item_id>', views.remove_basket, name="remove_basket"),
    path('orders/', views.user_orders, name="orders"),
    path('view_order/<int:order_id>', views.user_view_order, name="order"),
    path('view_complete_order/<int:order_id>', views.user_view_complete_order, name="complete_order")
]

handler404 = 'project_app.views.handler_404'
