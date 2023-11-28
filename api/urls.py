from django.urls import path
from rest_framework.routers import DefaultRouter
from api.views import *



router=DefaultRouter()
router.register('categories',CategoryView,basename='categories')
router.register('products',ProductView,basename='products')
router.register('mycart',CartsView,basename='mycart')
router.register('myorders',MyOrderView,basename='myorders')
router.register('orders',OrderView,basename='orders')

urlpatterns=[


]+router.urls