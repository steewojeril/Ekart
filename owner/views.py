from typing import Any, Dict
from django.db.models.query import QuerySet
from django.shortcuts import render,redirect
from owner.models import Orders,Products,Categories
from owner.forms import OrderUpdateForm,CategoryForm,ProductForm
from django.views.generic import TemplateView,ListView,DetailView,CreateView
from owner.decorators import super_sign_in_required
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
from django.urls import reverse_lazy

@method_decorator(super_sign_in_required,name='dispatch')
class AdminDashboard(TemplateView):
    template_name='owner/index.html'

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        count=Orders.objects.filter(status='order_placed').count()
        context['recent_order_count']=count
        count=Orders.objects.filter(status='delivered').count()
        context['delivered_count']=count
        count=Orders.objects.filter(status='dispatched').count()
        context['dispatch_count']=count
        count=Orders.objects.filter(status='in_transit').count()
        context['intransit_count']=count

        return context

@method_decorator(super_sign_in_required,name='dispatch')
class DeliveredView(ListView):
    model=Orders
    context_object_name='orders'
    template_name='owner/pending_request.html'

    def get_queryset(self):
        return Orders.objects.filter(status='delivered').order_by('-created_date')
    
@method_decorator(super_sign_in_required,name='dispatch')
class RecentOrders(ListView):
    model=Orders
    context_object_name='orders'
    template_name='owner/pending_request.html'
    
    def get_queryset(self):
        return Orders.objects.filter(status='order_placed').order_by('-created_date')
    
@method_decorator(super_sign_in_required,name='dispatch')
class DispatchedView(ListView):
    model=Orders
    context_object_name='orders'
    template_name='owner/pending_request.html'
    
    def get_queryset(self):
        return Orders.objects.filter(status='dispatched').order_by('-created_date')
    
@method_decorator(super_sign_in_required,name='dispatch')
class IntransitView(ListView):
    model=Orders
    context_object_name='orders'
    template_name='owner/pending_request.html'
    
    def get_queryset(self):
        return Orders.objects.filter(status='in_transit').order_by('-created_date')

@method_decorator(super_sign_in_required,name='dispatch')
class OrderDetailView(DetailView):
    model=Orders
    context_object_name='order'
    template_name='owner/order_details.html'
    pk_url_kwarg='id'
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        initial={
            'status':self.get_object().status,
            'expected_date':self.get_object().expected_date
        }
        context['form']=OrderUpdateForm(initial=initial)
        return context
    def post(self,request,*args,**kwargs):
        form=OrderUpdateForm(request.POST)
        order=self.get_object()
        if form.is_valid():
            status=form.cleaned_data.get('status')
            expected_date=form.cleaned_data.get('expected_date')
            # Update the order object with form data
            order.status=status
            order.expected_date=expected_date
            order.save()
            # order = form.save(commit=False)
            # order.save()  When you call form.save(commit=False), it creates an instance of the model associated with the form (in this case, Orders) using the data from the submitted form but does not save it to the database right away. Instead, it gives you the opportunity to perform any additional logic or modifications to the object before saving it.
            if order.status=='dispatched':
                matter=f"Your order {order.product.pro_name} of order value {order.product.price} has been dispatched. Expected date :{order.expected_date.strftime('%d/%m/%Y')}"
            elif order.status=='intransit':
                matter=f"Your order {order.product.pro_name} of order value {order.product.price} will be arrived on {order.expected_date.strftime('%d/%m/%Y')}"
            elif order.status=='delivered':
                matter=f"Your order {order.product.pro_name} of order value {order.product.price} has been delivered. Happy Shopping...."
            else:
                matter=f"something went wrong"
            self.send_delivery_status_email(matter) 
            return redirect('dashboard')
        return render(request,'owner/order_details.html',{'form':form})

    def send_delivery_status_email(self,matter):
            send_mail(
                'Order delivery status',
                matter,
                'steewoj@gmail.com',
                ['jeriljosec123@gmail.com'],
                fail_silently=True,
            )

@method_decorator(super_sign_in_required,name='dispatch')
class ProductDetailView(DetailView):
    template_name='owner/product_detail.html'
    model=Products
    context_object_name='product'
    pk_url_kwarg='id'

@method_decorator(super_sign_in_required,name='dispatch')
class ProductsListView(ListView):
    template_name='owner/product_list.html'
    model=Products
    context_object_name='products'


@method_decorator(super_sign_in_required,name='dispatch')
class CategoryAddView(CreateView):
    model=Categories
    form_class=CategoryForm
    template_name='owner/create_form.html'
    success_url=reverse_lazy('category_list')

@method_decorator(super_sign_in_required,name='dispatch')
class CategorysListView(ListView):
    template_name='owner/category_list.html'
    model=Categories
    context_object_name='categories'

@method_decorator(super_sign_in_required,name='dispatch')
class Category_ProductsListView(ListView):    
    def get(self,request,*args,**kwargs):
        id=kwargs.get('id')
        category=Categories.objects.get(id=id)
        products=Products.objects.filter(category=category)
        return render(request,'owner/product_list.html',{'products':products,'category_products':True,'category_inst':category.id})

@method_decorator(super_sign_in_required,name='dispatch')
class AddProductView(CreateView):
    model=Products
    form_class=ProductForm
    template_name='owner/create_form.html'
    success_url=reverse_lazy('product_list')
# to pass any value to the form-override get_initial mtd
    # def get_initial(self):
    #     initial = super().get_initial()
    #     id = self.kwargs.get('id')  # Assuming 'id' is the parameter name in the URL
    #     category = Categories.objects.get(id=id)  # Replace 'Category' with your actual Category model
    #     initial['category'] = category  # Set category as initial value for the form field
    #     return initial
    
# to save value to data base which is not passed throug the form
    def form_valid(self, form):
        id = self.kwargs.get('id')
        category = Categories.objects.get(id=id)
        form.instance.category = category 
        return super().form_valid(form)    
