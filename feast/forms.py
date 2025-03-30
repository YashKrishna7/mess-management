from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class SignInForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['name', 'description', 'price', 'category', 'available']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['menu_item', 'quantity']