from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price']


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_admin = False
        user.save()
        return user
