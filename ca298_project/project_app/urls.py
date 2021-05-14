from django.urls import path, include
from . import views
from .forms import UserLoginForm
from rest_framework import routers, serializers, viewsets
from .models import User, Product
from rest_framework.authtoken.views import obtain_auth_token


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'picture']


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = []
    permission_classes = []


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'products', views.ProductViewSet)

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
    path('view_complete_order/<int:order_id>', views.user_view_complete_order, name="complete_order"),
    path('api/', include(router.urls)),
    path('token/', obtain_auth_token, name="api_token_auth"),
    path('api_order/<int:order_id>', views.api_view_order, name="api_product_view")
]

handler404 = 'project_app.views.handler_404'
