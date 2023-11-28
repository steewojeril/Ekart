from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response 
from rest_framework import status
from django.shortcuts import render
from api.serializers import *
from owner.models import *
from rest_framework import viewsets 
from rest_framework import authentication,permissions

# def admin_check(fn):
#     def wrapperfn(self,request,*args,**kwargs):
#         if request.user.is_superuser:
#             return fn(self,request,*args,**kwargs)
#         else:
#             return Response({'msg':"you are not an admin"})
#     return wrapperfn




#.... only for admin users........permission_classes=[permissions.IsAdminUser].......
class CategoryView(viewsets.ModelViewSet):
    serializer_class=CategorySerializer
    queryset=Categories.objects.all()
    # authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAdminUser]

# url: api/ekart/categories/<pid>/add_product/
    @action(methods=["post"],detail=True)
    def add_product(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        category=Categories.objects.get(id=id)
        serializer=ProductSerializer(data=request.data,context={'category':category})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors)

# url: api/ekart/categories/<pid>/get_products/
    @action(methods=['get'],detail=True)
    def get_products(self,request,*args,**kwargs):
        try:
            id=kwargs.get('pk')
            category=Categories.objects.get(id=id)
            Products=category.products_set.all()
            serializer=ProductSerializer(Products,many=True)
            return Response(data=serializer.data,status=status.HTTP_200_OK)
        except:
            return Response({'msg':"doesn't exist"},status=status.HTTP_404_NOT_FOUND)


#....for both normal and  admin users......permission_classes=[permissions.IsAuthenticated].........
class ProductView(viewsets.ViewSet):
    # authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
# url: api/ekart/products/
    def list(self, request, *args, **kwargs):
        try:
            products=Products.objects.all()
            serializer=ProductSerializer(products,many=True)
            return Response(data=serializer.data,status=status.HTTP_200_OK)
        except:
            return Response({'msg':"doesn't exist"},status=status.HTTP_404_NOT_FOUND)

# url: api/ekart/products/<pid>/
    def retrieve(self, request, *args, **kwargs):
        try:
            id=kwargs.get('pk')
            product=Products.objects.get(id=id)
            serializer=ProductSerializer(product)
            return Response(data=serializer.data,status=status.HTTP_200_OK)
        except:
            return Response({'msg':"doesn't exist"},status=status.HTTP_404_NOT_FOUND)

# url: api/ekart/products/<pid>/add_to_cart/
    @action(methods=["post"],detail=True)
    def add_to_cart(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        product=Products.objects.get(id=id)
        user=request.user
        serializer=CartSerializer(data=request.data,context={"user":user,"product":product})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

# url: api/ekart/mycart/
class CartsView(viewsets.ModelViewSet):
    queryset = Carts.objects.all()
    serializer_class = CartSerializer
    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Carts.objects.filter(user=self.request.user,status='incart').order_by('-created_date')
    
    def destroy(self, request, *args, **kwargs):
        return Response({'msg':"not allowed"})
    def update(self, request, *args, **kwargs):
        return Response({'msg':"not allowed"})
    
# url: api/ekart/mycart/<pid>/remove_item/
    @action(methods=['put'],detail=True)
    def remove_item(self, request, *args, **kwargs):
        id=kwargs.get('pk')
        cart=Carts.objects.get(id=id)
        if cart.status!='cancelled':
            cart.status='cancelled'
            cart.save()
            return Response({"msg":'removed'})
        return Response({"msg":"doesn't exist"})
    
# url: api/ekart/mycart/create_order/
    @action(methods=['post'],detail=False)
    def create_order(self,request,*args,**kwargs):
        cart_instances=self.get_queryset().filter(status='incart')
        serializer=OrderSerializer(data=request.data,context={'user':request.user,'cart_instances':cart_instances})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
       


class MyOrderView(viewsets.ViewSet):
    # authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
# url: api/ekart/myorders/
    def list(self, request, *args, **kwargs):
        try:
            order_instances=Orders.objects.filter(user=self.request.user).exclude(status='cancelled').order_by('-created_date')
            serializer=OrderSerializer(order_instances,many=True)
            return Response(data=serializer.data,status=status.HTTP_200_OK)
        except:
            return Response({'msg':"doesn't exist"},status=status.HTTP_404_NOT_FOUND)




# url: api/ekart/orders/
# url: api/ekart/orders/<pid>
class OrderView(viewsets.ModelViewSet):
    serializer_class=OrderSerializer
    queryset=Orders.objects.all()
    # authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

# url: api/ekart/orders/
# url: api/ekart/orders?status={status}
    def list(self, request, *args, **kwargs):
        status=request.query_params.get('status')
        if status:
            order_instances=Orders.objects.filter(status=status)
            serializer=OrderSerializer(order_instances,many=True)
            return Response(data=serializer.data)
            
        return super().list(request, *args, **kwargs)
    
# url: api/ekart/orders/<pid>/update_status/
    @action(methods=["put"],detail=True)
    def update_status(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        order_instance=Orders.objects.get(id=id)
        serializer=OrderSerializer(data=request.data)
        if serializer.is_valid():
            order_instance.status=serializer.validated_data.get('status')
            order_instance.expected_date=serializer.validated_data.get('expected_date')
            order_instance.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)



    


