from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from owner.models import *

class RegistrationForm(UserCreationForm):
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model=User
        fields=['username','email','password1','password2']
        widgets={
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'})
        }

class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

class CartForm(forms.Form):
    qty=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control'}))
class CheckoutForm(forms.Form):
    address=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))