from owner.models import *
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Categories
        fields='__all__'

class ProductSerializer(serializers.ModelSerializer):
    category=serializers.CharField(read_only=True)
    class Meta:
        model=Products
        fields='__all__'
    def create(self, validated_data):
        category=self.context.get('category')
        return Products.objects.create(category=category,**validated_data)
    

class CartSerializer(serializers.ModelSerializer):
    user=serializers.CharField(read_only=True)
    product=serializers.CharField(read_only=True)

    class Meta:
        model=Carts
        fields='__all__'

    def create(self, validated_data):
        user=self.context.get("user")
        product=self.context.get("product")
        return Carts.objects.create(user=user,product=product,**validated_data)

class OrderSerializer(serializers.ModelSerializer):
    user=serializers.CharField(read_only=True)
    product=serializers.CharField(read_only=True)

    class Meta:
        model=Orders
        fields='__all__'

    def create(self, validated_data):
        cart_instances=self.context.get("cart_instances")
        user=self.context.get("user")
        for item in cart_instances:
            Orders.objects.create(user=user,product=item.product,quantity=item.quantity,**validated_data)
            item.status='order_placed'
            item.save()
        return object
