from typing import Any, Dict
from django.db import models
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render,redirect
from django.utils.decorators import method_decorator
from customer.decorators import sign_in_required
# Create your views here.
from customer import forms
from django.views.generic import CreateView,FormView,TemplateView,View,DetailView,ListView,UpdateView
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse_lazy
from owner.models import *
from django.contrib import messages

class RegistrationView(CreateView):
    form_class=forms.RegistrationForm
    template_name='registration.html'
    success_url=reverse_lazy('login')

class LoginView(FormView):
    form_class=forms.LoginForm
    template_name='login.html'

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        form=forms.LoginForm(request.POST)  # to take image > files=request.FILES
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(request,username=username,password=password)
            if user:
                login(request,user)
                if request.user.is_superuser:
                    messages.success(self.request,'You have been successfully Logged in. Welcome %s' %self.request.user)
                    return redirect('dashboard')
                else:
                    messages.success(self.request,'You have been successfully Logged in. Welcome %s' %self.request.user)
                    return redirect('home')
            else:
                return render(request,'login.html',{'form':form})
                
@method_decorator(sign_in_required,name='dispatch')
class HomeView(TemplateView):
    template_name='home.html'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        products=Products.objects.all()
        context['products']=products
        return context

    

@method_decorator(sign_in_required,name='dispatch')
class LogoutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        messages.success(request,'You have been succesfully logged out')
        return redirect('login')

@method_decorator(sign_in_required,name='dispatch')
class ProductDetailView(DetailView):
    template_name='pro_detail.html'
    model=Products
    context_object_name='product'
    pk_url_kwarg='id'

@method_decorator(sign_in_required,name='dispatch')
class AddToCart(FormView):
    form_class=forms.CartForm
    template_name='addtocart.html'
    def get(self, request, *args, **kwargs):
        id=kwargs.get('id')
        product=Products.objects.get(id=id)
        return render(request,self.template_name,{'form':self.form_class,'product':product})
    def post(self, request, *args, **kwargs):
        id=kwargs.get('id')
        product=Products.objects.get(id=id)
        user=request.user
        qty=request.POST.get('qty')
        Carts.objects.create(product=product,user=user,quantity=qty)
        messages.success(request,'Item has been succesfully added')
        return redirect('home')
    
@method_decorator(sign_in_required,name='dispatch')
class MyCartView(ListView):
    model=Carts
    template_name='mycart.html'
    context_object_name='carts'
    def get_queryset(self):
        return Carts.objects.filter(user=self.request.user,status='incart').order_by('-created_date')

@method_decorator(sign_in_required,name='dispatch')
class UpdateCartItem(View):
    def get(self, request, *args, **kwargs):
        id=kwargs.get('id')
        cart=Carts.objects.get(id=id)
        cart.status='cancelled'
        cart.save()
        messages.success(request,'Item has been removed from cart')
        return redirect('my_cart')

@method_decorator(sign_in_required,name='dispatch')
class UpdateOrderItem(View):
    def get(self, request, *args, **kwargs):
        id=kwargs.get('id')
        order=Orders.objects.get(id=id)
        order.status='cancelled'
        order.save()
        messages.success(request,'Your order ,%s has been cancelled' %order.product.pro_name)
        return redirect('myorders')

@method_decorator(sign_in_required,name='dispatch')
class MyOrderView(ListView):
    model=Orders
    template_name='myorders.html'
    context_object_name='orders'
    def get_queryset(self):
        return Orders.objects.filter(user=self.request.user).exclude(status='cancelled').order_by('-created_date')
    

@method_decorator(sign_in_required,name='dispatch')
class AddOrderView(FormView):
    form_class=forms.CheckoutForm
    template_name='checkout.html'
    def post(self, request,*args,**kwargs):
        form=forms.CheckoutForm(request.POST)
        if form.is_valid():
            address=form.cleaned_data.get('address')
            incart=request.user.carts_set.filter(user=request.user,status='incart')
            for item in incart:
                item.status='order_placed'
                item.save()
                Orders.objects.create(product=item.product,user=request.user,
                                    quantity=item.quantity,address=address)
            messages.success(request,'Your order has been placed')

        return redirect('myorders')
