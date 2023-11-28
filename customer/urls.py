from django.urls import path
from customer import views



urlpatterns=[
    path('',views.LoginView.as_view(),name='login'),
    path('register',views.RegistrationView.as_view(),name='register'),
    path('home',views.HomeView.as_view(),name='home'),
    path('logout',views.LogoutView.as_view(),name='logout'),
    path('products/<int:id>',views.ProductDetailView.as_view(),name='product_detail'),
    path('products/<int:id>/carts/add',views.AddToCart.as_view(),name='add_to_cart'),
    path('mycart',views.MyCartView.as_view(),name='my_cart'),
    path('cart/<int:id>/update',views.UpdateCartItem.as_view(),name='updatecart'),
    path('myorders',views.MyOrderView.as_view(),name='myorders'),
    # path('order',views.CheckoutView.as_view(),name='checkout'),
    path('order/<int:id>/update',views.UpdateOrderItem.as_view(),name='updateorder'),
    path('carts/placeorder',views.AddOrderView.as_view(),name='placeorder'),
]
