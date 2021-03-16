from django.forms import ModelForm, ModelChoiceField
from .models import Product, User, ProductCategory, Order, BasketItems
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django import forms
from django.contrib.auth.forms import AuthenticationForm


class CategoryChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class ProductForm(ModelForm):
    category = CategoryChoiceField(queryset=ProductCategory.objects.all())

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'picture', 'category']


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_admin = False
        user.save()
        return user


class AdminSignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_admin = True
        user.save()
        return user


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username', 'id': 'usernameInput'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'id': 'passwordInput'}))


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ["shipping_addr"]


class BasketItemForm(ModelForm):
    class Meta:
        model = BasketItems
        fields = ["message"]
