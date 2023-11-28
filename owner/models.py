from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator,MaxValueValidator
# Create your models here.
class Categories(models.Model):
    cat_name=models.CharField(max_length=200,unique=True)
    is_active=models.BooleanField(default=True)
# -> str  meanns expected return type of this method is string
    def __str__(self) -> str:
        return self.cat_name

class Products(models.Model):
    pro_name=models.CharField(max_length=200,unique=True)
    category=models.ForeignKey(Categories,on_delete=models.CASCADE)
    description=models.CharField(max_length=250,null=True)
    price=models.PositiveIntegerField()
    image=models.ImageField(upload_to='images',null=True,blank=True)

    def __str__(self) -> str:
        return self.pro_name
    
class Carts(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    created_date=models.DateTimeField(auto_now_add=True)
    options=(
        ('incart','In Cart'),
        ('order_placed','Order Placed'),
        ('cancelled','Cancelled')
    )
    status=models.CharField(max_length=120,choices=options,default='incart')

class Orders(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    created_date=models.DateTimeField(auto_now_add=True)
    options=(
        ('order_placed','Order Placed'),
        ('dispatched','Dispatched'),
        ('in_transit','In Transit'),
        ('delivered','Delivered'),
        ('cancelled','Cancelled')
    )
    status=models.CharField(max_length=120,choices=options,default='order_placed')
    address=models.CharField(max_length=200,null=True)
    expected_date=models.DateTimeField(null=True)

class Reviews(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    comments=models.CharField(max_length=200)
    rating=models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])